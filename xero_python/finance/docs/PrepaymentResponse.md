# PrepaymentResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prepayment_id** | **str** | Xero Identifier of prepayment | [optional] 
**contact** | [**ContactResponse**](ContactResponse.md) |  | [optional] 
**total** | **float** | Tax-inclusive total of the prepayment (SubTotal + TotalTax). Omitted in summary mode | [optional]
**line_items** | [**list[LineItemResponse]**](LineItemResponse.md) | Not included in summary mode | [optional] 

[[Back to README]](../../../README.md)


