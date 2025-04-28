Sub AverageAndStdDevAminoAcidValue()
    Dim ws As Worksheet
    Dim valueSum As Double
    Dim valueCount As Long
    Dim squaredDiffSum As Double
    Dim searchName As String
    Dim foundCell As Range
    Dim cellValue As Double
    Dim mean As Double
    Dim stdDev As Double

    ' Specify the amino acid name to search for
    searchName = "Target Amino Acid" ' Replace with the actual name

    valueSum = 0
    valueCount = 0
    squaredDiffSum = 0

    ' First pass: Calculate the sum and count of values
    For Each ws In ThisWorkbook.Worksheets
        On Error Resume Next
        ' Search for the amino acid name in Column A
        Set foundCell = ws.Columns("A").Find(What:=searchName, LookIn:=xlValues, LookAt:=xlWhole)
        If Not foundCell Is Nothing Then
            ' Get the corresponding value in Column B
            cellValue = ws.Cells(foundCell.Row, "B").Value
            If IsNumeric(cellValue) Then
                valueSum = valueSum + cellValue
                valueCount = valueCount + 1
            End If
        End If
        On Error GoTo 0
    Next ws

    ' Calculate the mean
    If valueCount > 0 Then
        mean = valueSum / valueCount

        ' Second pass: Calculate the sum of squared differences from the mean
        For Each ws In ThisWorkbook.Worksheets
            On Error Resume Next
            Set foundCell = ws.Columns("A").Find(What:=searchName, LookIn:=xlValues, LookAt:=xlWhole)
            If Not foundCell Is Nothing Then
                cellValue = ws.Cells(foundCell.Row, "B").Value
                If IsNumeric(cellValue) Then
                    squaredDiffSum = squaredDiffSum + (cellValue - mean) ^ 2
                End If
            End If
            On Error GoTo 0
        Next ws

        ' Calculate the standard deviation
        stdDev = Sqr(squaredDiffSum / valueCount)

        ' Display results
        MsgBox "The average value for '" & searchName & "' is: " & mean & vbNewLine & _
               "The standard deviation is: " & stdDev, vbInformation, "Calculation Results"
    Else
        MsgBox "No valid values found for '" & searchName & "' across sheets.", vbExclamation, "Error"
    End If
End Sub
