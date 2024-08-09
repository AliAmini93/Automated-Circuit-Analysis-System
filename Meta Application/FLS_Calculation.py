import math
XU = int(input("Is there any port on Up-side X of the board?: "))
XD = int(input("Is there any port on Down-side X of the board?: "))
YR = int(input("Is there any port on Right-side Y of the board?: "))
YL = int(input("Is there any port on Left-side Y of the board?: "))
##########################################
X0 = float(input("Enter X0: "))
Y0 = float(input("Enter Y0: "))
X_step = float(input("Enter X_step: "))
Y_step = float(input("Enter Y_step: "))
X_board = float(input("Enter X_board: "))
Y_board = float(input("Enter Y_board: "))

X_lense = 14
Y_lense = 22

X = [X0 + i*X_step for i in range(0, int((57 - X0)/X_step) + 1)]
Y = [Y0 + i*Y_step for i in range(0, int((40 - Y0)/Y_step) + 1)]

Xf = math.ceil(X0 + 2*X_step + X_board - X_lense)
Yf = math.ceil(Y0 + 2*Y_step + Y_board - Y_lense)

closest_Xi = max(filter(lambda x: x <= Xf, X))
closest_Yj = max(filter(lambda y: y <= Yf, Y))

##################################################
nX =  X.index(closest_Xi) + 1 if Xf in X else X.index(closest_Xi) + 2
nY = math.floor(closest_Yj/Y_step)+1 if Yf in Y else math.floor(Y[Y.index(closest_Yj) + 1]/Y_step)+1
##################################################
def ResX_Calculator():     
    CameraStartCoordinateX_OneToLast = X0 + (nX-2)*X_step
    CameraEndCoordinateX_OneToLast = CameraStartCoordinateX_OneToLast + X_lense
    ##################################################
    CircuitEndCoordinateX_OneToLast = X0 + X_step + X_board
    ##################################################
    ResX = CameraEndCoordinateX_OneToLast - CircuitEndCoordinateX_OneToLast
    print('ResX: ',ResX)
    return ResX
def ResY_Calculator():
    CameraStartCoordinateY_OneToLast = Y0 + (nY-2)*Y_step
    CameraEndCoordinateY_OneToLast = CameraStartCoordinateY_OneToLast + Y_lense
    ##################################################
    CircuitEndCoordinateY_OneToLast = Y0 + Y_step + Y_board
    ##################################################
    ResY = CameraEndCoordinateY_OneToLast - CircuitEndCoordinateY_OneToLast
    print('ResY: ',ResY)
    return ResY

rx =ResX_Calculator()
ry =ResY_Calculator()
if rx>=2:
    X_final = X_step * nX
    if (XD==1 and XU==1) or (XD==0 and XU==0):
        print(f'You can move the circuit in X direction {rx/2} cm.')
    if XU==1 and XD==0:
        print(f'You can move the circuit in X direction {rx-2} cm.')
    if XU==0 and XD==1:
        print('Do not move the circuit in X direction.')
else:
    print('Recalculating the ResX...')
    nX = nX + 1
    X_final = X_step * nX
    rx = ResX_Calculator()
    if (XD==1 and XU==1) or (XD==0 and XU==0):
        print(f'You can move the circuit in X direction {rx/2} cm.')
    if XU==1 and XD==0:
        print(f'You can move the circuit in X direction {rx/2} cm.')
    if XU==0 and XD==1:
        print(f'You can move the circuit in X direction {rx/2} cm.')
if ry>=2.5:
    Y_final = (nY-1) * Y_step + 1
    if (YR==1 and YL==1) or (YR==0 and YL==0):
        print(f'You can move the circuit in Y direction {ry/2} cm.')
    if YL==1 and YR==0:
        print(f'You can move the circuit in Y direction {ry-2} cm.')
    if YL==0 and YR==1:
        print('Do not move the circuit in Y direction.')
else:
    print('Recalculating the ResY...')
    nY = nY + 1
    Y_final = (nY -1)* Y_step + 1
    ry = ResY_Calculator()
    if (YR==1 and YL==1) or (YR==0 and YL==0):
        print(f'You can move the circuit in Y direction {ry/2} cm.')
    if YL==1 and YR==0:
        print(f'You can move the circuit in Y direction {ry/2} cm.')
    if YL==0 and YR==1:
        print(f'You can move the circuit in Y direction {ry/2} cm.')

#Y_final = math.floor(closest_Yj/Y_step)*Y_step + 1 if Yf in Y else math.floor(Y[Y.index(closest_Yj) + 1]/Y_step)*Y_step + 1
#X_final = X_step*(X.index(closest_Xi) + 1) if Xf in X else X_step*(X.index(closest_Xi) + 2)
#################################################################

print("X_final: ", X_final)
print("Y_final: ", Y_final)
