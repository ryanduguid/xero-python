# CreditNoteResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**credit_note_id** | **str** | Xero Identifier of credit note | [optional] 
**contact** | [**ContactResponse**](ContactResponse.md) |  | [optional] 
**total** | **float** | Tax-inclusive total of the credit note (SubTotal + TotalTax). Omitted in summary mode | [optional]
**line_items** | [**list[LineItemResponse]**](LineItemResponse.md) | Not included in summary mode | [optional] 

[[Back to README]](../../../README.md)


