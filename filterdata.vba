Sub Analyze_pKa_Data_Mac()
    Dim ws As Worksheet, summarySheet As Worksheet
    Dim groupName As String, pKaValue As Double
    Dim totalSheets As Integer, minSheets As Integer
    Dim lastRow As Long, i As Long
    Dim groupList() As String
    Dim pKaList() As Variant
    Dim groupCount() As Integer
    Dim uniqueGroups As Integer
    Dim rowIndex As Integer
    
    ' Initialize variables
    totalSheets = ThisWorkbook.Sheets.Count
    minSheets = totalSheets * 0.5 ' 50% threshold
    uniqueGroups = 0
    rowIndex = 2 ' Start row for summary output
    
    ' Loop through all sheets
    For Each ws In ThisWorkbook.Sheets
        ' Find last row with data in each sheet
        lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
        
        ' Loop through rows in each sheet
        For i = 2 To lastRow
            groupName = Trim(ws.Cells(i, 1).Value)
            If IsNumeric(ws.Cells(i, 2).Value) Then
                pKaValue = ws.Cells(i, 2).Value
                
                ' Check if pKa is within the specified range
                If pKaValue >= 6.8 And pKaValue <= 8# Then
                    ' Check if this group is already in the list, if not, add it
                    If Not IsInArray(groupName, groupList) Then
                        uniqueGroups = uniqueGroups + 1
                        ReDim Preserve groupList(1 To uniqueGroups)
                        ReDim Preserve pKaList(1 To uniqueGroups)
                        ReDim Preserve groupCount(1 To uniqueGroups)
                        groupList(uniqueGroups) = groupName
                        pKaList(uniqueGroups) = pKaValue
                        groupCount(uniqueGroups) = 1
                    Else
                        ' If the group is already in the list, add its pKa value
                        Dim groupIndex As Integer
                        groupIndex = GetGroupIndex(groupName, groupList)
                        pKaList(groupIndex) = pKaList(groupIndex) & "," & pKaValue
                        groupCount(groupIndex) = groupCount(groupIndex) + 1
                    End If
                End If
            End If
        Next i
    Next ws

    ' Create summary sheet
    On Error Resume Next
    Set summarySheet = ThisWorkbook.Sheets("Summary")
    If summarySheet Is Nothing Then
        Set summarySheet = ThisWorkbook.Sheets.Add
        summarySheet.Name = "Summary"
    End If
    On Error GoTo 0
    summarySheet.Cells.Clear

    ' Write headers to the summary sheet
    summarySheet.Cells(1, 1).Value = "Group"
    summarySheet.Cells(1, 2).Value = "Sheets Count"
    summarySheet.Cells(1, 3).Value = "Average pKa"
    summarySheet.Cells(1, 4).Value = "Standard Deviation"

    ' Loop through the groupList and calculate average and standard deviation
    For i = 1 To uniqueGroups
        If groupCount(i) >= minSheets Then
            Dim valuesArray() As Double
            Dim valuesStr() As String
            valuesStr = Split(pKaList(i), ",")
            ReDim valuesArray(0 To UBound(valuesStr))

            ' Convert values to an array of doubles
            Dim j As Integer
            For j = 0 To UBound(valuesStr)
                valuesArray(j) = CDbl(valuesStr(j))
            Next j

            ' Calculate average and standard deviation
            Dim avgValue As Double, stdDevValue As Double
            avgValue = Application.WorksheetFunction.Average(valuesArray)
            If UBound(valuesArray) > 0 Then
                stdDevValue = Application.WorksheetFunction.StDev(valuesArray)
            Else
                stdDevValue = 0
            End If

            ' Write to summary sheet
            summarySheet.Cells(rowIndex, 1).Value = groupList(i)
            summarySheet.Cells(rowIndex, 2).Value = groupCount(i)
            summarySheet.Cells(rowIndex, 3).Value = avgValue
            summarySheet.Cells(rowIndex, 4).Value = stdDevValue

            rowIndex = rowIndex + 1
        End If
    Next i

    MsgBox "Analysis complete! Summary saved in 'Summary' sheet.", vbInformation
End Sub

' Helper function to check if a value exists in an array
Function IsInArray(val As String, arr() As String) As Boolean
    Dim i As Integer
    On Error GoTo ErrHandler
    IsInArray = False
    For i = LBound(arr) To UBound(arr)
        If arr(i) = val Then
            IsInArray = True
            Exit Function
        End If
    Next i
    Exit Function
ErrHandler:
    IsInArray = False
End Function

' Helper function to get the index of a group in the array
Function GetGroupIndex(val As String, arr() As String) As Integer
    Dim i As Integer
    For i = LBound(arr) To UBound(arr)
        If arr(i) = val Then
            GetGroupIndex = i
            Exit Function
        End If
    Next i
    GetGroupIndex = -1 ' Return -1 if not found
End Function

