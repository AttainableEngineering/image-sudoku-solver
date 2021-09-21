# import for board print in main func.. delete later
from SudokuSolver import PrintBoard as pb

import cv2


import numpy as np


# import pytesseract to get string data from image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\closj\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def GetBoardFromAppSC(filename = "sudoku.jpg"):
    """
    Function:\nDesigned to crop a screenshot of sudoku board from
    \nsudoku2 app and pull sudoku board from image
    Inputs:
    \nfilename [str]: name of image file as a string - default "sudoku.jpg", an example case
    """
    # to print in openCV2 and close with an input press: 
    #   cv2.imshow("WindowName", imageVariable)
    #   cv2.waitKey(0)

    ### Image dimensions:
    '''
    pic total dim = 1792 x 828
    639 px to bottom of board
    410 px to top of board
    39 or 40 px to side of board
    11 px between cubes
    21 px between lines
    boxes 72 px wide

    top     (x) =   410 - 0     = 410 BUT added 3mm correction
    bottom  (w) =   1792 - 639  = 1153
    left    (y) =   40 - 0      = 40
    right   (h) =   828 - 40    = 788
    '''
    # Get pixel dims to crop and center board. 11 px offset to frame board for easy seperation into boxes.
    offset = 11 # px
    y = 43  - offset # left, 3mm correction from left to center outputs
    x = 410 - offset # top
    h = 788 + offset # right
    w = 1153 + offset # bottom

    # image = cv2.imread(filename)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Crop and center board
    crop_image = image[x:w, y:h]

    # cv2.imshow("board", crop_image)
    # cv2.waitKey(0)

    # ----------------- Begin Frame Image ---------------------------------
    # Create board to store rows for sudoku. Define the pixel width per box, dx.
    dx = 71
    board = []

    # Initialize counters for the space added between boxes and for row number.
    spacey = 0
    county = 0

    # Iterate through rows 1 - 9. Each new row, empty lists (rows) 
    for rows in range(1,10):
        lists = []
    
        # Set pixel value of spacey to account for thick horizontal lines, or otherwise to account for pixels between boxes, top and bottom.
        if county % 3 == 0 and county != 0:
            spacey += 24
        else:
            spacey += 10
        
        # Determine which row is being looked at to get correct framing on box, based on code above^^^
        county += 1
        
        # Get y framing pixel values to set top and bottom bounds for image check
        y2 = rows * dx + spacey
        y1 = y2 - dx 

        # Initialize counters for the space added between boxes and for column number
        spacex = 0
        countx = 0

        # Iterate through columns 1 - 9.
        for items in range(1,10):

            # Set pixel value of spacex to account for thick vertical lines, or otherwise to account for pixels between boxes, left and right.
            if countx % 3 == 0 and countx != 0:
                spacex += 24
            else:
                spacex += 10

            # Determine which member from the row is being looked at to get correct framing on box, based on code above^^^
            countx += 1

            # Get x framing pixel values to set left and right bounds for image check
            x2 = items * dx + spacex
            x1 = x2-dx

            # Get a region of interest around each square in the board to check for values 
            roi = crop_image[y1:y2, x1:x2]

            # Crop each region of interest to only include the region you care about
            ylen = abs(int(y2-y1))
            xlen = abs(int(x2-x1))
            yc1 = int(ylen/10)-5
            yc2 = int(9*ylen/10)+5
            xc1 = int(xlen/10)-2
            xc2 = int(9*xlen/10)+2
            cropped = roi[yc1:yc2, xc1:xc2]

            # cv2.imshow("AOI", roi)
            # cv2.waitKey(0)
            # ------------------ END FRAME IMAGE -----------------

            # Image Progessing
            #blur = cv2.GaussianBlur(roi, (17,17), 0)
            #blur = cv2.blur(roi, (7,7) )
            #step = cv2.bilateralFilter(roi, 9, 75, 75) # keep edges but get rid of wood background
            blur = cv2.GaussianBlur(cropped, (17,17), 0) # blur pixels together
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            sharpen_kernel = np.array([[1,1,1], [1,1,1], [1,1,1]])*1/7
            sharpen = cv2.filter2D(thresh, -1, sharpen_kernel)

            # # Uncomment below to print what the computer is seeing:
            # cv2.imshow("Processed", sharpen)
            # cv2.waitKey(0)

            # Search processed image for text
            data = pytesseract.image_to_string(sharpen, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789')
            # # Uncomment below to print out what pytesseract sees in the square:
            # print(data)

            # 71x71 pixels in images, find the total number of white pixels, compare to threshhold, and determine if blob or number
            totalwhite = cv2.countNonZero(thresh)   # NOTE, white really black pixels, but image is inverted... it's white for us in the viewfield
            totalpixel = 5041
            whitepercent = (totalwhite / totalpixel)*100
            threshhold = 54 ## NOTE - Adjust value as needed for sensitivity... Increase means more black

            if whitepercent < threshhold:
                # data is suspected to not be a number, despite pytesseract. Invalidate any data output.
                data = 0

            

            # If the value detected can be converted to an integer, add it to the board. Otherwise add a 0 to the board
            try:
                lists.append(int(data))
            except:
                lists.append(0)

        # Append the newly finished list to the board
        board.append(lists)
    
    # Once all lists are appended to the board, return the board
    return board
######## END FUNCTION DEFINITION


example1 = [
    [4, 0, 8, 0, 0, 6, 3, 0, 0],
    [3, 0, 0, 7, 0, 0, 0, 0, 0],
    [2, 0, 0, 4, 0, 5, 0, 0, 0],
    [0, 0, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 6, 2, 0, 0, 0, 0, 0],
    [5, 2, 0, 9, 0, 0, 8, 0, 7],
    [0, 4, 0, 8, 0, 2, 5, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 8, 0],
    [7, 0, 0, 0, 1, 3, 0, 6, 0]
]

example2 = [
    [4, 0, 0, 2, 0, 0, 7, 0, 0],
    [0, 0, 9, 0, 1, 0, 5, 0, 0],
    [0, 0, 7, 3, 0, 5, 2, 0, 4],
    [1, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 9, 0, 0, 8, 0, 0],
    [9, 0, 8, 0, 7, 0, 0, 0, 0],
    [0, 4, 0, 5, 0, 0, 0, 0, 8],
    [0, 5, 0, 4, 3, 0, 9, 0, 2]
]

example3 = [
    [8, 0, 0, 6, 0, 0, 0, 3, 7],
    [0, 6, 0, 2, 0, 0, 0, 0, 4],
    [0, 5, 3, 0, 0, 0, 6, 0, 0],
    [0, 8, 2, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 8, 1, 0, 0, 5, 6],
    [0, 0, 0, 0, 0, 7, 0, 0, 5],
    [4, 0, 0, 0, 2, 0, 3, 7, 0],
    [0, 0, 0, 0, 3, 0, 0, 1, 0]
]

def CheckExample(example, filehandle = "sudoku.jpg"):
    '''
    Error checking sequence with predefined board.

    '''
    

    # Get board from default sudoku board to compare to example variable
    outboard = GetBoardFromAppSC(filehandle)
    pb(outboard)
    print(" ")
    
    errorcount = 0

    # Iterate and count thru rows and columns
    rowcount = 0
    for rows in outboard:
        rowcount += 1
        colcount = 0
        for columns in rows:
            colcount += 1
            # Check for errors. Return locations. 
            if columns != example[rowcount-1][colcount-1]:
                errorcount += 1
                print("Error on entry [" + str(rowcount) + ", " + str(colcount) + "]", end = " ")
                print("\n(Row:", rowcount, end=" ")
                print("Column: " + str(colcount) + ")")
                print("Expecting:", example[rowcount-1][colcount-1], end = " ")
                print("but got " + str(columns) + " instead...\n")

    # Return status of error testing
    if errorcount == 0:
        print("\nNo Errors\n")
    else:
        print("Threw " + str(errorcount) + " error(s)...\n")


if __name__ == "__main__":
    print("\nRunning Test Sequence:\n")
    print("Example 1:")
    CheckExample(example1)
    print("Example 2:")
    CheckExample(example2, "sudoku2.jpg")    
    print("Example 3:")
    CheckExample(example3, "sudoku3.jpg")