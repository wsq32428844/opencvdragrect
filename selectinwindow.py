# MIT License

# Copyright (c) 2021 Akshay Chavan

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cv2
import math


class Rect:
    x = None
    y = None
    w = None
    h = None

    def printit(self):
        print(str(self.x) + ',' + str(self.y) + ',' + str(self.w) + ',' + str(self.h))


class DragRectangle:
    # Limits on the canvas
    keepWithin = Rect()
    # To store rectangle
    outRect = Rect()
    # To store rectangle anchor point
    # Here the rect class object is used to store
    # the distance in the x and y direction from
    # the anchor point to the top-left and the bottom-right corner
    anchor = Rect()
    # Selection marker size
    sBlk = 4
    # Whether initialized or not
    initialized = False

    # Image
    image = None

    # Window Name
    wname = ""

    # Return flag
    returnflag = False

    # FLAGS
    # Rect already present
    active = False
    # Drag for rect resize in progress
    drag = False
    # Marker flags by positions
    TL = False
    TM = False
    TR = False
    LM = False
    RM = False
    BL = False
    BM = False
    BR = False
    hold = False
    # Rotation flag
    rotating = False
    # Current rotation angle in degrees
    angle = 0
    # Center of the rectangle for rotation
    center = (0, 0)
    # Initial rectangle angle when rotation starts
    initial_rectangle_angle = 0
    # Initial mouse angle when rotation starts
    initial_mouse_angle = 0

    def __init__(self, Img, windowName, windowWidth, windowHeight):
        # Image
        self.image = Img

        # Window name
        self.wname = windowName

        # Limit the selection box to the canvas
        self.keepWithin.x = 0
        self.keepWithin.y = 0
        self.keepWithin.w = windowWidth
        self.keepWithin.h = windowHeight

        # Set rect to zero width and height
        self.outRect.x = 0
        self.outRect.y = 0
        self.outRect.w = 0
        self.outRect.h = 0


def dragrect(event, x, y, flags, dragObj):
    if x < dragObj.keepWithin.x:
        x = dragObj.keepWithin.x
    if y < dragObj.keepWithin.y:
        y = dragObj.keepWithin.y
    if x > (dragObj.keepWithin.x + dragObj.keepWithin.w - 1):
        x = dragObj.keepWithin.x + dragObj.keepWithin.w - 1
    if y > (dragObj.keepWithin.y + dragObj.keepWithin.h - 1):
        y = dragObj.keepWithin.y + dragObj.keepWithin.h - 1

    if event == cv2.EVENT_LBUTTONDOWN:
        mouseDown(x, y, dragObj)
    if event == cv2.EVENT_LBUTTONUP:
        mouseUp(dragObj)
    if event == cv2.EVENT_MOUSEMOVE:
        mouseMove(x, y, dragObj)
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseDoubleClick(x, y, dragObj)
    if event == cv2.EVENT_RBUTTONDOWN:
        mouseRightDown(x, y, dragObj)
    if event == cv2.EVENT_RBUTTONUP:
        mouseRightUp(dragObj)


def pointInRect(pX, pY, rX, rY, rW, rH):
    if rX <= pX <= (rX + rW) and rY <= pY <= (rY + rH):
        return True
    else:
        return False


def mouseDoubleClick(eX, eY, dragObj):
    if dragObj.active:
        if pointInRect(eX, eY, dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h):
            dragObj.returnflag = True
            cv2.destroyWindow(dragObj.wname)


def mouseDown(eX, eY, dragObj):
    if dragObj.active:
        if pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                       dragObj.outRect.y - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.TL = True
            return
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                       dragObj.outRect.y - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.TR = True
            return
        if pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.BL = True
            return
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.BR = True
            return

        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk,
                       dragObj.outRect.y - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.TM = True
            return
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w / 2 - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.BM = True
            return
        if pointInRect(eX, eY, dragObj.outRect.x - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.LM = True
            return
        if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                       dragObj.outRect.y + dragObj.outRect.h / 2 - dragObj.sBlk,
                       dragObj.sBlk * 2, dragObj.sBlk * 2):
            dragObj.RM = True
            return

        # This has to be below all of the other conditions
        if pointInRect(eX, eY, dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h):
            dragObj.anchor.x = eX - dragObj.outRect.x
            dragObj.anchor.w = dragObj.outRect.w - dragObj.anchor.x
            dragObj.anchor.y = eY - dragObj.outRect.y
            dragObj.anchor.h = dragObj.outRect.h - dragObj.anchor.y
            dragObj.hold = True

            return

    else:
        dragObj.outRect.x = eX
        dragObj.outRect.y = eY
        dragObj.drag = True
        dragObj.active = True
        return


def mouseMove(eX, eY, dragObj):
    if dragObj.rotating:
        # Calculate the vector from center to current mouse position
        dx = eX - dragObj.center[0]
        dy = eY - dragObj.center[1]
        
        # Calculate the current mouse angle from the x-axis
        current_mouse_angle = math.degrees(math.atan2(dy, dx))
        
        # Calculate the rotation delta from the initial mouse angle
        delta_angle = current_mouse_angle - dragObj.initial_mouse_angle
        
        # Update the rectangle's angle (cumulative)
        dragObj.angle = dragObj.initial_rectangle_angle + delta_angle
        print(f"Rotation: initial_mouse={dragObj.initial_mouse_angle:.2f}, current_mouse={current_mouse_angle:.2f}, delta={delta_angle:.2f}, total_angle={dragObj.angle:.2f}")
        clearCanvasNDraw(dragObj)
        return

    if dragObj.drag & dragObj.active:
        dragObj.outRect.w = eX - dragObj.outRect.x
        dragObj.outRect.h = eY - dragObj.outRect.y
        clearCanvasNDraw(dragObj)
        return

    if dragObj.hold:
        dragObj.outRect.x = eX - dragObj.anchor.x
        dragObj.outRect.y = eY - dragObj.anchor.y

        if dragObj.outRect.x < dragObj.keepWithin.x:
            dragObj.outRect.x = dragObj.keepWithin.x
        if dragObj.outRect.y < dragObj.keepWithin.y:
            dragObj.outRect.y = dragObj.keepWithin.y
        if (dragObj.outRect.x + dragObj.outRect.w) > (dragObj.keepWithin.x + dragObj.keepWithin.w - 1):
            dragObj.outRect.x = dragObj.keepWithin.x + dragObj.keepWithin.w - 1 - dragObj.outRect.w
        if (dragObj.outRect.y + dragObj.outRect.h) > (dragObj.keepWithin.y + dragObj.keepWithin.h - 1):
            dragObj.outRect.y = dragObj.keepWithin.y + dragObj.keepWithin.h - 1 - dragObj.outRect.h

        clearCanvasNDraw(dragObj)
        return

    if dragObj.TL:
        dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
        dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
        dragObj.outRect.x = eX
        dragObj.outRect.y = eY
        clearCanvasNDraw(dragObj)
        return
    if dragObj.BR:
        dragObj.outRect.w = eX - dragObj.outRect.x
        dragObj.outRect.h = eY - dragObj.outRect.y
        clearCanvasNDraw(dragObj)
        return
    if dragObj.TR:
        dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
        dragObj.outRect.y = eY
        dragObj.outRect.w = eX - dragObj.outRect.x
        clearCanvasNDraw(dragObj)
        return
    if dragObj.BL:
        dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
        dragObj.outRect.x = eX
        dragObj.outRect.h = eY - dragObj.outRect.y
        clearCanvasNDraw(dragObj)
        return

    if dragObj.TM:
        dragObj.outRect.h = (dragObj.outRect.y + dragObj.outRect.h) - eY
        dragObj.outRect.y = eY
        clearCanvasNDraw(dragObj)
        return
    if dragObj.BM:
        dragObj.outRect.h = eY - dragObj.outRect.y
        clearCanvasNDraw(dragObj)
        return
    if dragObj.LM:
        dragObj.outRect.w = (dragObj.outRect.x + dragObj.outRect.w) - eX
        dragObj.outRect.x = eX
        clearCanvasNDraw(dragObj)
        return
    if dragObj.RM:
        dragObj.outRect.w = eX - dragObj.outRect.x
        clearCanvasNDraw(dragObj)
        return


def mouseUp(dragObj):
    dragObj.drag = False
    disableResizeButtons(dragObj)
    straightenUpRect(dragObj)
    if dragObj.outRect.w == 0 or dragObj.outRect.h == 0:
        dragObj.active = False

    clearCanvasNDraw(dragObj)

def mouseRightDown(eX, eY, dragObj):
    print(f"Right-click detected at ({eX}, {eY})")
    if dragObj.active:
        # Calculate the center of the rectangle
        centerX = dragObj.outRect.x + dragObj.outRect.w // 2
        centerY = dragObj.outRect.y + dragObj.outRect.h // 2
        
        # Check if right-click on top-right marker
        marker_found = False
        
        if dragObj.angle != 0:
            # Calculate the rotated top-right vertex
            theta = math.radians(dragObj.angle)
            # Original top-right vertex
            tr_x = dragObj.outRect.x + dragObj.outRect.w
            tr_y = dragObj.outRect.y
            # Rotate around center
            rotated_tr_x = centerX + (tr_x - centerX) * math.cos(theta) - (tr_y - centerY) * math.sin(theta)
            rotated_tr_y = centerY + (tr_x - centerX) * math.sin(theta) + (tr_y - centerY) * math.cos(theta)
            
            # Check if mouse is near the rotated top-right marker
            if pointInRect(eX, eY, rotated_tr_x - dragObj.sBlk,
                           rotated_tr_y - dragObj.sBlk,
                           dragObj.sBlk * 2, dragObj.sBlk * 2):
                marker_found = True
        else:
            # Check if right-click on top-right marker (original position)
            if pointInRect(eX, eY, dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                           dragObj.outRect.y - dragObj.sBlk,
                           dragObj.sBlk * 2, dragObj.sBlk * 2):
                marker_found = True
        
        if marker_found:
            dragObj.center = (centerX, centerY)
            # Calculate initial mouse angle from center to mouse position
            dx_initial = eX - centerX
            dy_initial = eY - centerY
            dragObj.initial_mouse_angle = math.degrees(math.atan2(dy_initial, dx_initial))
            # Store the current rectangle angle
            dragObj.initial_rectangle_angle = dragObj.angle
            dragObj.rotating = True
            print(f"Rotation started: center={dragObj.center}, initial_mouse_angle={dragObj.initial_mouse_angle}, initial_rectangle_angle={dragObj.initial_rectangle_angle}")

def mouseRightUp(dragObj):
    dragObj.rotating = False


def disableResizeButtons(dragObj):
    dragObj.TL = dragObj.TM = dragObj.TR = False
    dragObj.LM = dragObj.RM = False
    dragObj.BL = dragObj.BM = dragObj.BR = False
    dragObj.hold = False


def straightenUpRect(dragObj):
    """
    Make sure x, y, w, h of the Rect are positive
    """
    if dragObj.outRect.w < 0:
        dragObj.outRect.x = dragObj.outRect.x + dragObj.outRect.w
        dragObj.outRect.w = -dragObj.outRect.w
    if dragObj.outRect.h < 0:
        dragObj.outRect.y = dragObj.outRect.y + dragObj.outRect.h
        dragObj.outRect.h = -dragObj.outRect.h


def clearCanvasNDraw(dragObj):
    # Draw
    tmp = dragObj.image.copy()
    
    # Get rectangle parameters
    x, y, w, h = dragObj.outRect.x, dragObj.outRect.y, dragObj.outRect.w, dragObj.outRect.h
    
    if dragObj.angle != 0:
        # Calculate the center of the rectangle
        center = (x + w // 2, y + h // 2)
        
        # Create rotation matrix
        M = cv2.getRotationMatrix2D(center, dragObj.angle, 1.0)
        
        # Calculate the four vertices of the rectangle
        pts = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype=np.float32)
        
        # Rotate the vertices
        rotated_pts = cv2.transform(np.array([pts]), M)[0]
        
        # Draw the rotated rectangle
        cv2.polylines(tmp, [np.int32(rotated_pts)], True, (0, 255, 0), 2)
        
        # Update drawSelectMarkers to handle rotation
        drawSelectMarkers(tmp, dragObj, rotated_pts)
    else:
        # Draw regular rectangle
        cv2.rectangle(tmp, (x, y), (x + w, y + h), (0, 255, 0), 2)
        drawSelectMarkers(tmp, dragObj)
    
    # Display the image without waiting for a key
    cv2.imshow(dragObj.wname, tmp)
    # Use a very short wait time to avoid recursion
    cv2.waitKey(1)


def drawSelectMarkers(image, dragObj, rotated_pts=None):
    """
    Draw markers on the dragged rectangle
    """
    if rotated_pts is None:
        # Top-Left
        cv2.rectangle(image, (dragObj.outRect.x - dragObj.sBlk,
                              dragObj.outRect.y - dragObj.sBlk),
                      (dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)
        # Top-Rigth
        cv2.rectangle(image, (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                              dragObj.outRect.y - dragObj.sBlk),
                      (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)
        # Bottom-Left
        cv2.rectangle(image, (dragObj.outRect.x - dragObj.sBlk,
                              dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk),
                      (dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)
        # Bottom-Right
        cv2.rectangle(image, (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                              dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk),
                      (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)

        # Top-Mid
        cv2.rectangle(image, (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk,
                              dragObj.outRect.y - dragObj.sBlk),
                      (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)
        # Bottom-Mid
        cv2.rectangle(image, (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk,
                              dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk),
                      (dragObj.outRect.x + int(dragObj.outRect.w / 2) - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y + dragObj.outRect.h - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)
        # Left-Mid
        cv2.rectangle(image, (dragObj.outRect.x - dragObj.sBlk,
                              dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk),
                      (dragObj.outRect.x - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)
        # Right-Mid
        cv2.rectangle(image, (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk,
                              dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk),
                      (dragObj.outRect.x + dragObj.outRect.w - dragObj.sBlk + dragObj.sBlk * 2,
                       dragObj.outRect.y + int(dragObj.outRect.h / 2) - dragObj.sBlk + dragObj.sBlk * 2),
                      (0, 255, 0), 2)
    else:
        # Calculate marker positions for rotated rectangle
        # Top-Left, Top-Right, Bottom-Right, Bottom-Left
        tl, tr, br, bl = rotated_pts
        
        # Draw corner markers
        markers = [tl, tr, br, bl]
        for pt in markers:
            x, y = int(pt[0]), int(pt[1])
            cv2.rectangle(image, (x - dragObj.sBlk, y - dragObj.sBlk),
                          (x + dragObj.sBlk, y + dragObj.sBlk), (0, 255, 0), 2)
        
        # Draw midpoint markers
        # Top-Mid
        tm_x = int((tl[0] + tr[0]) / 2)
        tm_y = int((tl[1] + tr[1]) / 2)
        cv2.rectangle(image, (tm_x - dragObj.sBlk, tm_y - dragObj.sBlk),
                      (tm_x + dragObj.sBlk, tm_y + dragObj.sBlk), (0, 255, 0), 2)
        
        # Bottom-Mid
        bm_x = int((bl[0] + br[0]) / 2)
        bm_y = int((bl[1] + br[1]) / 2)
        cv2.rectangle(image, (bm_x - dragObj.sBlk, bm_y - dragObj.sBlk),
                      (bm_x + dragObj.sBlk, bm_y + dragObj.sBlk), (0, 255, 0), 2)
        
        # Left-Mid
        lm_x = int((tl[0] + bl[0]) / 2)
        lm_y = int((tl[1] + bl[1]) / 2)
        cv2.rectangle(image, (lm_x - dragObj.sBlk, lm_y - dragObj.sBlk),
                      (lm_x + dragObj.sBlk, lm_y + dragObj.sBlk), (0, 255, 0), 2)
        
        # Right-Mid
        rm_x = int((tr[0] + br[0]) / 2)
        rm_y = int((tr[1] + br[1]) / 2)
        cv2.rectangle(image, (rm_x - dragObj.sBlk, rm_y - dragObj.sBlk),
                      (rm_x + dragObj.sBlk, rm_y + dragObj.sBlk), (0, 255, 0), 2)
