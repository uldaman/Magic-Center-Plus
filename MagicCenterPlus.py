import c4d


def Join(op, doc):
    res = c4d.utils.SendModelingCommand(command=c4d.MCOMMAND_JOIN,
                                        list=[op],
                                        mode=c4d.MODELINGCOMMANDMODE_ALL,
                                        bc=c4d.BaseContainer(),
                                        doc=doc)
    if res:
        return res[0]


def CenterObj(obj):  # Center obj's axis
    doc = c4d.documents.GetActiveDocument()  # Get active Cinema 4D document
    Joined = Join(obj, doc)
    if Joined:
        Joined.SetMg(c4d.Matrix())  # Reset poly's global matrix
        CenterPoly(Joined)
        obj.SetMg(Joined.GetMg())  # Set obj's global matrix
        Joined.Remove()


def CenterPoly(op):  # Center poly's axis
    points = []  # Initialize empty list
    pointCount = op.GetPointCount()  # Get poly's point count
    for i in range(0, pointCount):  # Loop through points
        points.append(op.GetPoint(i))  # Add point to points list
    matrix = op.GetMg()  # Get poly's global matrix
    center = op.GetMp()  # Get poly's bounding box center in local space
    axis = op.GetAbsPos()  # Get poly's absolute position
    difference = axis - (axis + center)  # Calculate difference
    if difference != c4d.Vector(0):  # If there is a difference
        for i in range(pointCount):  # Loop through poly's points
            op.SetPoint(i, points[i] + difference)  # Set new point position
        op.Message(c4d.MSG_UPDATE)  # Send update message
        op.SetMg(c4d.Matrix((matrix * center),
                            matrix.v1, matrix.v2, matrix.v3))  # Set new matrix for the poly


def main():
    doc = c4d.documents.GetActiveDocument()  # Get active Cinema 4D document
    doc.StartUndo()  # Start recording undos
    try:  # Try to execute following script
        selection = doc.GetActiveObjects(
            c4d.GETACTIVEOBJECTFLAGS_CHILDREN)  # Get active objects
        for obj in selection:  # Loop through selection

            childrenMat = []  # Initialize list for children matrices
            children = obj.GetChildren()  # Get object's children
            for child in children:  # Iterate through children
                childMat = child.GetMg()  # Get child's matrix
                childrenMat.append(childMat)  # Add matrix to the matrices list

            # Add undo command for making changes to object
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)

            # If selected object is non-editable
            if not obj.CheckType(c4d.Opoint):
                CenterObj(obj)
            else:  # Otherwise
                CenterPoly(obj)

            for i, child in enumerate(children):  # Iterate through children
                child.SetMg(childrenMat[i])  # Reset matrix

    except:  # If something goes wront
        pass  # Do nothing
    doc.EndUndo()  # Stop recording undos
    c4d.EventAdd()  # Refresh Cinema 4D


# Execute main()
if __name__ == '__main__':
    main()
