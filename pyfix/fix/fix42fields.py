# automatically generated, do not edit

# (source: FIX42.xml)

from pyfix.fix.context import FixFieldDescriptor, FixGroupDescriptor

__all__ = ['FIX_HEADER_FIELD_IDS', 'FIX_TRAILER_FIELD_IDS', '_fix_field_types', '_fix_message_types', '_fix_group_types', '_fix_field_numbers', '_fix_group_numbers', '_fix_msgtype_table']

FIX_HEADER_FIELD_IDS = [
	8, 9, 35, 49, 56, 115, 128, 90, 91, 34, 50, 142, 57, 143, 116, 144, 129, 145, 43, 97, 52, 122, 212, 213, 347, 369, 370]

FIX_TRAILER_FIELD_IDS = [10, 89, 93]

_fix_field_types = {
	'Account': FixFieldDescriptor('Account', 1, 'STRING', str),
	'AccruedInterestAmt': FixFieldDescriptor('AccruedInterestAmt', 159, 'AMT', float),
	'AccruedInterestRate': FixFieldDescriptor('AccruedInterestRate', 158, 'FLOAT', float),
	'Adjustment': FixFieldDescriptor('Adjustment', 334, 'INT', int),
	'AdvId': FixFieldDescriptor('AdvId', 2, 'STRING', str),
	'AdvRefID': FixFieldDescriptor('AdvRefID', 3, 'STRING', str),
	'AdvSide': FixFieldDescriptor('AdvSide', 4, 'CHAR', str),
	'AdvTransType': FixFieldDescriptor('AdvTransType', 5, 'STRING', str),
	'AggregatedBook': FixFieldDescriptor('AggregatedBook', 266, 'BOOLEAN', str),
	'AllocAccount': FixFieldDescriptor('AllocAccount', 79, 'STRING', str),
	'AllocAvgPx': FixFieldDescriptor('AllocAvgPx', 153, 'PRICE', float),
	'AllocHandlInst': FixFieldDescriptor('AllocHandlInst', 209, 'INT', int),
	'AllocID': FixFieldDescriptor('AllocID', 70, 'STRING', str),
	'AllocLinkID': FixFieldDescriptor('AllocLinkID', 196, 'STRING', str),
	'AllocLinkType': FixFieldDescriptor('AllocLinkType', 197, 'INT', int),
	'AllocNetMoney': FixFieldDescriptor('AllocNetMoney', 154, 'AMT', float),
	'AllocPrice': FixFieldDescriptor('AllocPrice', 366, 'PRICE', float),
	'AllocRejCode': FixFieldDescriptor('AllocRejCode', 88, 'INT', int),
	'AllocShares': FixFieldDescriptor('AllocShares', 80, 'QTY', float),
	'AllocStatus': FixFieldDescriptor('AllocStatus', 87, 'INT', int),
	'AllocText': FixFieldDescriptor('AllocText', 161, 'STRING', str),
	'AllocTransType': FixFieldDescriptor('AllocTransType', 71, 'CHAR', str),
	'AvgPrxPrecision': FixFieldDescriptor('AvgPrxPrecision', 74, 'INT', int),
	'AvgPx': FixFieldDescriptor('AvgPx', 6, 'PRICE', float),
	'BasisPxType': FixFieldDescriptor('BasisPxType', 419, 'CHAR', str),
	'BeginSeqNo': FixFieldDescriptor('BeginSeqNo', 7, 'INT', int),
	'BeginString': FixFieldDescriptor('BeginString', 8, 'STRING', str),
	'Benchmark': FixFieldDescriptor('Benchmark', 219, 'CHAR', str),
	'BidDescriptor': FixFieldDescriptor('BidDescriptor', 400, 'STRING', str),
	'BidDescriptorType': FixFieldDescriptor('BidDescriptorType', 399, 'INT', int),
	'BidForwardPoints': FixFieldDescriptor('BidForwardPoints', 189, 'PRICEOFFSET', float),
	'BidID': FixFieldDescriptor('BidID', 390, 'STRING', str),
	'BidPx': FixFieldDescriptor('BidPx', 132, 'PRICE', float),
	'BidRequestTransType': FixFieldDescriptor('BidRequestTransType', 374, 'CHAR', str),
	'BidSize': FixFieldDescriptor('BidSize', 134, 'QTY', float),
	'BidSpotRate': FixFieldDescriptor('BidSpotRate', 188, 'PRICE', float),
	'BidType': FixFieldDescriptor('BidType', 394, 'INT', int),
	'BodyLength': FixFieldDescriptor('BodyLength', 9, 'INT', int),
	'BrokerOfCredit': FixFieldDescriptor('BrokerOfCredit', 92, 'STRING', str),
	'BusinessRejectReason': FixFieldDescriptor('BusinessRejectReason', 380, 'INT', int),
	'BusinessRejectRefID': FixFieldDescriptor('BusinessRejectRefID', 379, 'STRING', str),
	'BuyVolume': FixFieldDescriptor('BuyVolume', 330, 'QTY', float),
	'CashOrderQty': FixFieldDescriptor('CashOrderQty', 152, 'QTY', float),
	'CashSettlAgentAcctName': FixFieldDescriptor('CashSettlAgentAcctName', 185, 'STRING', str),
	'CashSettlAgentAcctNum': FixFieldDescriptor('CashSettlAgentAcctNum', 184, 'STRING', str),
	'CashSettlAgentCode': FixFieldDescriptor('CashSettlAgentCode', 183, 'STRING', str),
	'CashSettlAgentContactName': FixFieldDescriptor('CashSettlAgentContactName', 186, 'STRING', str),
	'CashSettlAgentContactPhone': FixFieldDescriptor('CashSettlAgentContactPhone', 187, 'STRING', str),
	'CashSettlAgentName': FixFieldDescriptor('CashSettlAgentName', 182, 'STRING', str),
	'CheckSum': FixFieldDescriptor('CheckSum', 10, 'STRING', str),
	'ClOrdID': FixFieldDescriptor('ClOrdID', 11, 'STRING', str),
	'ClearingAccount': FixFieldDescriptor('ClearingAccount', 440, 'STRING', str),
	'ClearingFirm': FixFieldDescriptor('ClearingFirm', 439, 'STRING', str),
	'ClientBidID': FixFieldDescriptor('ClientBidID', 391, 'STRING', str),
	'ClientID': FixFieldDescriptor('ClientID', 109, 'STRING', str),
	'CommType': FixFieldDescriptor('CommType', 13, 'CHAR', str),
	'Commission': FixFieldDescriptor('Commission', 12, 'AMT', float),
	'ComplianceID': FixFieldDescriptor('ComplianceID', 376, 'STRING', str),
	'ContraBroker': FixFieldDescriptor('ContraBroker', 375, 'STRING', str),
	'ContraTradeQty': FixFieldDescriptor('ContraTradeQty', 437, 'QTY', float),
	'ContraTradeTime': FixFieldDescriptor('ContraTradeTime', 438, 'UTCTIMESTAMP', str),
	'ContraTrader': FixFieldDescriptor('ContraTrader', 337, 'STRING', str),
	'ContractMultiplier': FixFieldDescriptor('ContractMultiplier', 231, 'FLOAT', float),
	'CorporateAction': FixFieldDescriptor('CorporateAction', 292, 'CHAR', str),
	'Country': FixFieldDescriptor('Country', 421, 'STRING', str),
	'CouponRate': FixFieldDescriptor('CouponRate', 223, 'FLOAT', float),
	'CoveredOrUncovered': FixFieldDescriptor('CoveredOrUncovered', 203, 'INT', int),
	'CrossPercent': FixFieldDescriptor('CrossPercent', 413, 'FLOAT', float),
	'CumQty': FixFieldDescriptor('CumQty', 14, 'QTY', float),
	'Currency': FixFieldDescriptor('Currency', 15, 'CURRENCY', str),
	'CustomerOrFirm': FixFieldDescriptor('CustomerOrFirm', 204, 'INT', int),
	'CxlQty': FixFieldDescriptor('CxlQty', 84, 'QTY', float),
	'CxlRejReason': FixFieldDescriptor('CxlRejReason', 102, 'INT', int),
	'CxlRejResponseTo': FixFieldDescriptor('CxlRejResponseTo', 434, 'CHAR', str),
	'CxlType': FixFieldDescriptor('CxlType', 125, 'CHAR', str),
	'DKReason': FixFieldDescriptor('DKReason', 127, 'CHAR', str),
	'DayAvgPx': FixFieldDescriptor('DayAvgPx', 426, 'PRICE', float),
	'DayCumQty': FixFieldDescriptor('DayCumQty', 425, 'QTY', float),
	'DayOrderQty': FixFieldDescriptor('DayOrderQty', 424, 'QTY', float),
	'DefBidSize': FixFieldDescriptor('DefBidSize', 293, 'QTY', float),
	'DefOfferSize': FixFieldDescriptor('DefOfferSize', 294, 'QTY', float),
	'DeleteReason': FixFieldDescriptor('DeleteReason', 285, 'CHAR', str),
	'DeliverToCompID': FixFieldDescriptor('DeliverToCompID', 128, 'STRING', str),
	'DeliverToLocationID': FixFieldDescriptor('DeliverToLocationID', 145, 'STRING', str),
	'DeliverToSubID': FixFieldDescriptor('DeliverToSubID', 129, 'STRING', str),
	'DeskID': FixFieldDescriptor('DeskID', 284, 'STRING', str),
	'DiscretionInst': FixFieldDescriptor('DiscretionInst', 388, 'CHAR', str),
	'DiscretionOffset': FixFieldDescriptor('DiscretionOffset', 389, 'PRICEOFFSET', float),
	'DlvyInst': FixFieldDescriptor('DlvyInst', 86, 'STRING', str),
	'DueToRelated': FixFieldDescriptor('DueToRelated', 329, 'BOOLEAN', str),
	'EFPTrackingError': FixFieldDescriptor('EFPTrackingError', 405, 'FLOAT', float),
	'EffectiveTime': FixFieldDescriptor('EffectiveTime', 168, 'UTCTIMESTAMP', str),
	'EmailThreadID': FixFieldDescriptor('EmailThreadID', 164, 'STRING', str),
	'EmailType': FixFieldDescriptor('EmailType', 94, 'CHAR', str),
	'EncodedAllocText': FixFieldDescriptor('EncodedAllocText', 361, 'DATA', str),
	'EncodedAllocTextLen': FixFieldDescriptor('EncodedAllocTextLen', 360, 'INT', int),
	'EncodedHeadline': FixFieldDescriptor('EncodedHeadline', 359, 'DATA', str),
	'EncodedHeadlineLen': FixFieldDescriptor('EncodedHeadlineLen', 358, 'INT', int),
	'EncodedIssuer': FixFieldDescriptor('EncodedIssuer', 349, 'DATA', str),
	'EncodedIssuerLen': FixFieldDescriptor('EncodedIssuerLen', 348, 'INT', int),
	'EncodedListExecInst': FixFieldDescriptor('EncodedListExecInst', 353, 'DATA', str),
	'EncodedListExecInstLen': FixFieldDescriptor('EncodedListExecInstLen', 352, 'INT', int),
	'EncodedListStatusText': FixFieldDescriptor('EncodedListStatusText', 446, 'DATA', str),
	'EncodedListStatusTextLen': FixFieldDescriptor('EncodedListStatusTextLen', 445, 'INT', int),
	'EncodedSecurityDesc': FixFieldDescriptor('EncodedSecurityDesc', 351, 'DATA', str),
	'EncodedSecurityDescLen': FixFieldDescriptor('EncodedSecurityDescLen', 350, 'INT', int),
	'EncodedSubject': FixFieldDescriptor('EncodedSubject', 357, 'DATA', str),
	'EncodedSubjectLen': FixFieldDescriptor('EncodedSubjectLen', 356, 'INT', int),
	'EncodedText': FixFieldDescriptor('EncodedText', 355, 'DATA', str),
	'EncodedTextLen': FixFieldDescriptor('EncodedTextLen', 354, 'INT', int),
	'EncodedUnderlyingIssuer': FixFieldDescriptor('EncodedUnderlyingIssuer', 363, 'DATA', str),
	'EncodedUnderlyingIssuerLen': FixFieldDescriptor('EncodedUnderlyingIssuerLen', 362, 'INT', int),
	'EncodedUnderlyingSecurityDesc': FixFieldDescriptor('EncodedUnderlyingSecurityDesc', 365, 'DATA', str),
	'EncodedUnderlyingSecurityDescLen': FixFieldDescriptor('EncodedUnderlyingSecurityDescLen', 364, 'INT', int),
	'EncryptMethod': FixFieldDescriptor('EncryptMethod', 98, 'INT', int),
	'EndSeqNo': FixFieldDescriptor('EndSeqNo', 16, 'INT', int),
	'ExDestination': FixFieldDescriptor('ExDestination', 100, 'EXCHANGE', str),
	'ExchangeForPhysical': FixFieldDescriptor('ExchangeForPhysical', 411, 'BOOLEAN', str),
	'ExecBroker': FixFieldDescriptor('ExecBroker', 76, 'STRING', str),
	'ExecID': FixFieldDescriptor('ExecID', 17, 'STRING', str),
	'ExecInst': FixFieldDescriptor('ExecInst', 18, 'MULTIPLEVALUESTRING', str),
	'ExecRefID': FixFieldDescriptor('ExecRefID', 19, 'STRING', str),
	'ExecRestatementReason': FixFieldDescriptor('ExecRestatementReason', 378, 'INT', int),
	'ExecTransType': FixFieldDescriptor('ExecTransType', 20, 'CHAR', str),
	'ExecType': FixFieldDescriptor('ExecType', 150, 'CHAR', str),
	'ExpireDate': FixFieldDescriptor('ExpireDate', 432, 'LOCALMKTDATE', str),
	'ExpireTime': FixFieldDescriptor('ExpireTime', 126, 'UTCTIMESTAMP', str),
	'FairValue': FixFieldDescriptor('FairValue', 406, 'AMT', float),
	'FinancialStatus': FixFieldDescriptor('FinancialStatus', 291, 'CHAR', str),
	'ForexReq': FixFieldDescriptor('ForexReq', 121, 'BOOLEAN', str),
	'FutSettDate': FixFieldDescriptor('FutSettDate', 64, 'LOCALMKTDATE', str),
	'FutSettDate2': FixFieldDescriptor('FutSettDate2', 193, 'LOCALMKTDATE', str),
	'GTBookingInst': FixFieldDescriptor('GTBookingInst', 427, 'INT', int),
	'GapFillFlag': FixFieldDescriptor('GapFillFlag', 123, 'BOOLEAN', str),
	'GrossTradeAmt': FixFieldDescriptor('GrossTradeAmt', 381, 'AMT', float),
	'HaltReason': FixFieldDescriptor('HaltReason', 327, 'CHAR', str),
	'HandlInst': FixFieldDescriptor('HandlInst', 21, 'CHAR', str),
	'Headline': FixFieldDescriptor('Headline', 148, 'STRING', str),
	'HeartBtInt': FixFieldDescriptor('HeartBtInt', 108, 'INT', int),
	'HighPx': FixFieldDescriptor('HighPx', 332, 'PRICE', float),
	'IDSource': FixFieldDescriptor('IDSource', 22, 'STRING', str),
	'IOINaturalFlag': FixFieldDescriptor('IOINaturalFlag', 130, 'BOOLEAN', str),
	'IOIOthSvc': FixFieldDescriptor('IOIOthSvc', 24, 'CHAR', str),
	'IOIQltyInd': FixFieldDescriptor('IOIQltyInd', 25, 'CHAR', str),
	'IOIQualifier': FixFieldDescriptor('IOIQualifier', 104, 'CHAR', str),
	'IOIRefID': FixFieldDescriptor('IOIRefID', 26, 'STRING', str),
	'IOIShares': FixFieldDescriptor('IOIShares', 27, 'STRING', str),
	'IOITransType': FixFieldDescriptor('IOITransType', 28, 'CHAR', str),
	'IOIid': FixFieldDescriptor('IOIid', 23, 'STRING', str),
	'InViewOfCommon': FixFieldDescriptor('InViewOfCommon', 328, 'BOOLEAN', str),
	'IncTaxInd': FixFieldDescriptor('IncTaxInd', 416, 'INT', int),
	'Issuer': FixFieldDescriptor('Issuer', 106, 'STRING', str),
	'LastCapacity': FixFieldDescriptor('LastCapacity', 29, 'CHAR', str),
	'LastForwardPoints': FixFieldDescriptor('LastForwardPoints', 195, 'PRICEOFFSET', float),
	'LastMkt': FixFieldDescriptor('LastMkt', 30, 'EXCHANGE', str),
	'LastMsgSeqNumProcessed': FixFieldDescriptor('LastMsgSeqNumProcessed', 369, 'INT', int),
	'LastPx': FixFieldDescriptor('LastPx', 31, 'PRICE', float),
	'LastShares': FixFieldDescriptor('LastShares', 32, 'QTY', float),
	'LastSpotRate': FixFieldDescriptor('LastSpotRate', 194, 'PRICE', float),
	'LeavesQty': FixFieldDescriptor('LeavesQty', 151, 'QTY', float),
	'LinesOfText': FixFieldDescriptor('LinesOfText', 33, 'INT', int),
	'LiquidityIndType': FixFieldDescriptor('LiquidityIndType', 409, 'INT', int),
	'LiquidityNumSecurities': FixFieldDescriptor('LiquidityNumSecurities', 441, 'INT', int),
	'LiquidityPctHigh': FixFieldDescriptor('LiquidityPctHigh', 403, 'FLOAT', float),
	'LiquidityPctLow': FixFieldDescriptor('LiquidityPctLow', 402, 'FLOAT', float),
	'LiquidityValue': FixFieldDescriptor('LiquidityValue', 404, 'AMT', float),
	'ListExecInst': FixFieldDescriptor('ListExecInst', 69, 'STRING', str),
	'ListExecInstType': FixFieldDescriptor('ListExecInstType', 433, 'CHAR', str),
	'ListID': FixFieldDescriptor('ListID', 66, 'STRING', str),
	'ListName': FixFieldDescriptor('ListName', 392, 'STRING', str),
	'ListOrderStatus': FixFieldDescriptor('ListOrderStatus', 431, 'INT', int),
	'ListSeqNo': FixFieldDescriptor('ListSeqNo', 67, 'INT', int),
	'ListStatusText': FixFieldDescriptor('ListStatusText', 444, 'STRING', str),
	'ListStatusType': FixFieldDescriptor('ListStatusType', 429, 'INT', int),
	'LocateReqd': FixFieldDescriptor('LocateReqd', 114, 'BOOLEAN', str),
	'LocationID': FixFieldDescriptor('LocationID', 283, 'STRING', str),
	'LowPx': FixFieldDescriptor('LowPx', 333, 'PRICE', float),
	'MDEntryBuyer': FixFieldDescriptor('MDEntryBuyer', 288, 'STRING', str),
	'MDEntryDate': FixFieldDescriptor('MDEntryDate', 272, 'UTCDATE', str),
	'MDEntryID': FixFieldDescriptor('MDEntryID', 278, 'STRING', str),
	'MDEntryOriginator': FixFieldDescriptor('MDEntryOriginator', 282, 'STRING', str),
	'MDEntryPositionNo': FixFieldDescriptor('MDEntryPositionNo', 290, 'INT', int),
	'MDEntryPx': FixFieldDescriptor('MDEntryPx', 270, 'PRICE', float),
	'MDEntryRefID': FixFieldDescriptor('MDEntryRefID', 280, 'STRING', str),
	'MDEntrySeller': FixFieldDescriptor('MDEntrySeller', 289, 'STRING', str),
	'MDEntrySize': FixFieldDescriptor('MDEntrySize', 271, 'QTY', float),
	'MDEntryTime': FixFieldDescriptor('MDEntryTime', 273, 'UTCTIMEONLY', str),
	'MDEntryType': FixFieldDescriptor('MDEntryType', 269, 'CHAR', str),
	'MDMkt': FixFieldDescriptor('MDMkt', 275, 'EXCHANGE', str),
	'MDReqID': FixFieldDescriptor('MDReqID', 262, 'STRING', str),
	'MDReqRejReason': FixFieldDescriptor('MDReqRejReason', 281, 'CHAR', str),
	'MDUpdateAction': FixFieldDescriptor('MDUpdateAction', 279, 'CHAR', str),
	'MDUpdateType': FixFieldDescriptor('MDUpdateType', 265, 'INT', int),
	'MarketDepth': FixFieldDescriptor('MarketDepth', 264, 'INT', int),
	'MaturityDay': FixFieldDescriptor('MaturityDay', 205, 'DAYOFMONTH', int),
	'MaturityMonthYear': FixFieldDescriptor('MaturityMonthYear', 200, 'MONTHYEAR', str),
	'MaxFloor': FixFieldDescriptor('MaxFloor', 111, 'QTY', float),
	'MaxMessageSize': FixFieldDescriptor('MaxMessageSize', 383, 'INT', int),
	'MaxShow': FixFieldDescriptor('MaxShow', 210, 'QTY', float),
	'MessageEncoding': FixFieldDescriptor('MessageEncoding', 347, 'STRING', str),
	'MinQty': FixFieldDescriptor('MinQty', 110, 'QTY', float),
	'MiscFeeAmt': FixFieldDescriptor('MiscFeeAmt', 137, 'AMT', float),
	'MiscFeeCurr': FixFieldDescriptor('MiscFeeCurr', 138, 'CURRENCY', str),
	'MiscFeeType': FixFieldDescriptor('MiscFeeType', 139, 'CHAR', str),
	'MsgDirection': FixFieldDescriptor('MsgDirection', 385, 'CHAR', str),
	'MsgSeqNum': FixFieldDescriptor('MsgSeqNum', 34, 'INT', int),
	'MsgType': FixFieldDescriptor('MsgType', 35, 'STRING', str),
	'MultiLegReportingType': FixFieldDescriptor('MultiLegReportingType', 442, 'CHAR', str),
	'NetGrossInd': FixFieldDescriptor('NetGrossInd', 430, 'INT', int),
	'NetMoney': FixFieldDescriptor('NetMoney', 118, 'AMT', float),
	'NewSeqNo': FixFieldDescriptor('NewSeqNo', 36, 'INT', int),
	'NoAllocs': FixFieldDescriptor('NoAllocs', 78, 'INT', int),
	'NoBidComponents': FixFieldDescriptor('NoBidComponents', 420, 'INT', int),
	'NoBidDescriptors': FixFieldDescriptor('NoBidDescriptors', 398, 'INT', int),
	'NoContraBrokers': FixFieldDescriptor('NoContraBrokers', 382, 'INT', int),
	'NoDlvyInst': FixFieldDescriptor('NoDlvyInst', 85, 'INT', int),
	'NoExecs': FixFieldDescriptor('NoExecs', 124, 'INT', int),
	'NoIOIQualifiers': FixFieldDescriptor('NoIOIQualifiers', 199, 'INT', int),
	'NoMDEntries': FixFieldDescriptor('NoMDEntries', 268, 'INT', int),
	'NoMDEntryTypes': FixFieldDescriptor('NoMDEntryTypes', 267, 'INT', int),
	'NoMiscFees': FixFieldDescriptor('NoMiscFees', 136, 'INT', int),
	'NoMsgTypes': FixFieldDescriptor('NoMsgTypes', 384, 'INT', int),
	'NoOrders': FixFieldDescriptor('NoOrders', 73, 'INT', int),
	'NoQuoteEntries': FixFieldDescriptor('NoQuoteEntries', 295, 'INT', int),
	'NoQuoteSets': FixFieldDescriptor('NoQuoteSets', 296, 'INT', int),
	'NoRelatedSym': FixFieldDescriptor('NoRelatedSym', 146, 'INT', int),
	'NoRoutingIDs': FixFieldDescriptor('NoRoutingIDs', 215, 'INT', int),
	'NoRpts': FixFieldDescriptor('NoRpts', 82, 'INT', int),
	'NoStrikes': FixFieldDescriptor('NoStrikes', 428, 'INT', int),
	'NoTradingSessions': FixFieldDescriptor('NoTradingSessions', 386, 'INT', int),
	'NotifyBrokerOfCredit': FixFieldDescriptor('NotifyBrokerOfCredit', 208, 'BOOLEAN', str),
	'NumBidders': FixFieldDescriptor('NumBidders', 417, 'INT', int),
	'NumDaysInterest': FixFieldDescriptor('NumDaysInterest', 157, 'INT', int),
	'NumTickets': FixFieldDescriptor('NumTickets', 395, 'INT', int),
	'NumberOfOrders': FixFieldDescriptor('NumberOfOrders', 346, 'INT', int),
	'OfferForwardPoints': FixFieldDescriptor('OfferForwardPoints', 191, 'PRICEOFFSET', float),
	'OfferPx': FixFieldDescriptor('OfferPx', 133, 'PRICE', float),
	'OfferSize': FixFieldDescriptor('OfferSize', 135, 'QTY', float),
	'OfferSpotRate': FixFieldDescriptor('OfferSpotRate', 190, 'PRICE', float),
	'OnBehalfOfCompID': FixFieldDescriptor('OnBehalfOfCompID', 115, 'STRING', str),
	'OnBehalfOfLocationID': FixFieldDescriptor('OnBehalfOfLocationID', 144, 'STRING', str),
	'OnBehalfOfSendingTime': FixFieldDescriptor('OnBehalfOfSendingTime', 370, 'UTCTIMESTAMP', str),
	'OnBehalfOfSubID': FixFieldDescriptor('OnBehalfOfSubID', 116, 'STRING', str),
	'OpenClose': FixFieldDescriptor('OpenClose', 77, 'CHAR', str),
	'OpenCloseSettleFlag': FixFieldDescriptor('OpenCloseSettleFlag', 286, 'CHAR', str),
	'OptAttribute': FixFieldDescriptor('OptAttribute', 206, 'CHAR', str),
	'OrdRejReason': FixFieldDescriptor('OrdRejReason', 103, 'INT', int),
	'OrdStatus': FixFieldDescriptor('OrdStatus', 39, 'CHAR', str),
	'OrdType': FixFieldDescriptor('OrdType', 40, 'CHAR', str),
	'OrderID': FixFieldDescriptor('OrderID', 37, 'STRING', str),
	'OrderQty': FixFieldDescriptor('OrderQty', 38, 'QTY', float),
	'OrderQty2': FixFieldDescriptor('OrderQty2', 192, 'QTY', float),
	'OrigClOrdID': FixFieldDescriptor('OrigClOrdID', 41, 'STRING', str),
	'OrigSendingTime': FixFieldDescriptor('OrigSendingTime', 122, 'UTCTIMESTAMP', str),
	'OrigTime': FixFieldDescriptor('OrigTime', 42, 'UTCTIMESTAMP', str),
	'OutMainCntryUIndex': FixFieldDescriptor('OutMainCntryUIndex', 412, 'AMT', float),
	'OutsideIndexPct': FixFieldDescriptor('OutsideIndexPct', 407, 'FLOAT', float),
	'PegDifference': FixFieldDescriptor('PegDifference', 211, 'PRICEOFFSET', float),
	'PossDupFlag': FixFieldDescriptor('PossDupFlag', 43, 'BOOLEAN', str),
	'PossResend': FixFieldDescriptor('PossResend', 97, 'BOOLEAN', str),
	'PrevClosePx': FixFieldDescriptor('PrevClosePx', 140, 'PRICE', float),
	'Price': FixFieldDescriptor('Price', 44, 'PRICE', float),
	'PriceType': FixFieldDescriptor('PriceType', 423, 'INT', int),
	'ProcessCode': FixFieldDescriptor('ProcessCode', 81, 'CHAR', str),
	'ProgPeriodInterval': FixFieldDescriptor('ProgPeriodInterval', 415, 'INT', int),
	'ProgRptReqs': FixFieldDescriptor('ProgRptReqs', 414, 'INT', int),
	'PutOrCall': FixFieldDescriptor('PutOrCall', 201, 'INT', int),
	'QuoteAckStatus': FixFieldDescriptor('QuoteAckStatus', 297, 'INT', int),
	'QuoteCancelType': FixFieldDescriptor('QuoteCancelType', 298, 'INT', int),
	'QuoteCondition': FixFieldDescriptor('QuoteCondition', 276, 'MULTIPLEVALUESTRING', str),
	'QuoteEntryID': FixFieldDescriptor('QuoteEntryID', 299, 'STRING', str),
	'QuoteEntryRejectReason': FixFieldDescriptor('QuoteEntryRejectReason', 368, 'INT', int),
	'QuoteID': FixFieldDescriptor('QuoteID', 117, 'STRING', str),
	'QuoteRejectReason': FixFieldDescriptor('QuoteRejectReason', 300, 'INT', int),
	'QuoteReqID': FixFieldDescriptor('QuoteReqID', 131, 'STRING', str),
	'QuoteRequestType': FixFieldDescriptor('QuoteRequestType', 303, 'INT', int),
	'QuoteResponseLevel': FixFieldDescriptor('QuoteResponseLevel', 301, 'INT', int),
	'QuoteSetID': FixFieldDescriptor('QuoteSetID', 302, 'STRING', str),
	'QuoteSetValidUntilTime': FixFieldDescriptor('QuoteSetValidUntilTime', 367, 'UTCTIMESTAMP', str),
	'RatioQty': FixFieldDescriptor('RatioQty', 319, 'QTY', float),
	'RawData': FixFieldDescriptor('RawData', 96, 'DATA', str),
	'RawDataLength': FixFieldDescriptor('RawDataLength', 95, 'INT', int),
	'RefAllocID': FixFieldDescriptor('RefAllocID', 72, 'STRING', str),
	'RefMsgType': FixFieldDescriptor('RefMsgType', 372, 'STRING', str),
	'RefSeqNum': FixFieldDescriptor('RefSeqNum', 45, 'INT', int),
	'RefTagID': FixFieldDescriptor('RefTagID', 371, 'INT', int),
	'RelatdSym': FixFieldDescriptor('RelatdSym', 46, 'STRING', str),
	'ReportToExch': FixFieldDescriptor('ReportToExch', 113, 'BOOLEAN', str),
	'ResetSeqNumFlag': FixFieldDescriptor('ResetSeqNumFlag', 141, 'BOOLEAN', str),
	'RoutingID': FixFieldDescriptor('RoutingID', 217, 'STRING', str),
	'RoutingType': FixFieldDescriptor('RoutingType', 216, 'INT', int),
	'RptSeq': FixFieldDescriptor('RptSeq', 83, 'INT', int),
	'Rule80A': FixFieldDescriptor('Rule80A', 47, 'CHAR', str),
	'SecondaryOrderID': FixFieldDescriptor('SecondaryOrderID', 198, 'STRING', str),
	'SecureData': FixFieldDescriptor('SecureData', 91, 'DATA', str),
	'SecureDataLen': FixFieldDescriptor('SecureDataLen', 90, 'INT', int),
	'SecurityDesc': FixFieldDescriptor('SecurityDesc', 107, 'STRING', str),
	'SecurityExchange': FixFieldDescriptor('SecurityExchange', 207, 'EXCHANGE', str),
	'SecurityID': FixFieldDescriptor('SecurityID', 48, 'STRING', str),
	'SecurityReqID': FixFieldDescriptor('SecurityReqID', 320, 'STRING', str),
	'SecurityRequestType': FixFieldDescriptor('SecurityRequestType', 321, 'INT', int),
	'SecurityResponseID': FixFieldDescriptor('SecurityResponseID', 322, 'STRING', str),
	'SecurityResponseType': FixFieldDescriptor('SecurityResponseType', 323, 'INT', int),
	'SecuritySettlAgentAcctName': FixFieldDescriptor('SecuritySettlAgentAcctName', 179, 'STRING', str),
	'SecuritySettlAgentAcctNum': FixFieldDescriptor('SecuritySettlAgentAcctNum', 178, 'STRING', str),
	'SecuritySettlAgentCode': FixFieldDescriptor('SecuritySettlAgentCode', 177, 'STRING', str),
	'SecuritySettlAgentContactName': FixFieldDescriptor('SecuritySettlAgentContactName', 180, 'STRING', str),
	'SecuritySettlAgentContactPhone': FixFieldDescriptor('SecuritySettlAgentContactPhone', 181, 'STRING', str),
	'SecuritySettlAgentName': FixFieldDescriptor('SecuritySettlAgentName', 176, 'STRING', str),
	'SecurityStatusReqID': FixFieldDescriptor('SecurityStatusReqID', 324, 'STRING', str),
	'SecurityTradingStatus': FixFieldDescriptor('SecurityTradingStatus', 326, 'INT', int),
	'SecurityType': FixFieldDescriptor('SecurityType', 167, 'STRING', str),
	'SellVolume': FixFieldDescriptor('SellVolume', 331, 'QTY', float),
	'SellerDays': FixFieldDescriptor('SellerDays', 287, 'INT', int),
	'SenderCompID': FixFieldDescriptor('SenderCompID', 49, 'STRING', str),
	'SenderLocationID': FixFieldDescriptor('SenderLocationID', 142, 'STRING', str),
	'SenderSubID': FixFieldDescriptor('SenderSubID', 50, 'STRING', str),
	'SendingTime': FixFieldDescriptor('SendingTime', 52, 'UTCTIMESTAMP', str),
	'SessionRejectReason': FixFieldDescriptor('SessionRejectReason', 373, 'INT', int),
	'SettlBrkrCode': FixFieldDescriptor('SettlBrkrCode', 174, 'STRING', str),
	'SettlCurrAmt': FixFieldDescriptor('SettlCurrAmt', 119, 'AMT', float),
	'SettlCurrFxRate': FixFieldDescriptor('SettlCurrFxRate', 155, 'FLOAT', float),
	'SettlCurrFxRateCalc': FixFieldDescriptor('SettlCurrFxRateCalc', 156, 'CHAR', str),
	'SettlCurrency': FixFieldDescriptor('SettlCurrency', 120, 'CURRENCY', str),
	'SettlDeliveryType': FixFieldDescriptor('SettlDeliveryType', 172, 'INT', int),
	'SettlDepositoryCode': FixFieldDescriptor('SettlDepositoryCode', 173, 'STRING', str),
	'SettlInstCode': FixFieldDescriptor('SettlInstCode', 175, 'STRING', str),
	'SettlInstID': FixFieldDescriptor('SettlInstID', 162, 'STRING', str),
	'SettlInstMode': FixFieldDescriptor('SettlInstMode', 160, 'CHAR', str),
	'SettlInstRefID': FixFieldDescriptor('SettlInstRefID', 214, 'STRING', str),
	'SettlInstSource': FixFieldDescriptor('SettlInstSource', 165, 'CHAR', str),
	'SettlInstTransType': FixFieldDescriptor('SettlInstTransType', 163, 'CHAR', str),
	'SettlLocation': FixFieldDescriptor('SettlLocation', 166, 'STRING', str),
	'SettlmntTyp': FixFieldDescriptor('SettlmntTyp', 63, 'CHAR', str),
	'Shares': FixFieldDescriptor('Shares', 53, 'QTY', float),
	'Side': FixFieldDescriptor('Side', 54, 'CHAR', str),
	'SideValue1': FixFieldDescriptor('SideValue1', 396, 'AMT', float),
	'SideValue2': FixFieldDescriptor('SideValue2', 397, 'AMT', float),
	'SideValueInd': FixFieldDescriptor('SideValueInd', 401, 'INT', int),
	'Signature': FixFieldDescriptor('Signature', 89, 'DATA', str),
	'SignatureLength': FixFieldDescriptor('SignatureLength', 93, 'INT', int),
	'SolicitedFlag': FixFieldDescriptor('SolicitedFlag', 377, 'BOOLEAN', str),
	'SpreadToBenchmark': FixFieldDescriptor('SpreadToBenchmark', 218, 'PRICEOFFSET', float),
	'StandInstDbID': FixFieldDescriptor('StandInstDbID', 171, 'STRING', str),
	'StandInstDbName': FixFieldDescriptor('StandInstDbName', 170, 'STRING', str),
	'StandInstDbType': FixFieldDescriptor('StandInstDbType', 169, 'INT', int),
	'StopPx': FixFieldDescriptor('StopPx', 99, 'PRICE', float),
	'StrikePrice': FixFieldDescriptor('StrikePrice', 202, 'PRICE', float),
	'StrikeTime': FixFieldDescriptor('StrikeTime', 443, 'UTCTIMESTAMP', str),
	'Subject': FixFieldDescriptor('Subject', 147, 'STRING', str),
	'SubscriptionRequestType': FixFieldDescriptor('SubscriptionRequestType', 263, 'CHAR', str),
	'Symbol': FixFieldDescriptor('Symbol', 55, 'STRING', str),
	'SymbolSfx': FixFieldDescriptor('SymbolSfx', 65, 'STRING', str),
	'TargetCompID': FixFieldDescriptor('TargetCompID', 56, 'STRING', str),
	'TargetLocationID': FixFieldDescriptor('TargetLocationID', 143, 'STRING', str),
	'TargetSubID': FixFieldDescriptor('TargetSubID', 57, 'STRING', str),
	'TestReqID': FixFieldDescriptor('TestReqID', 112, 'STRING', str),
	'Text': FixFieldDescriptor('Text', 58, 'STRING', str),
	'TickDirection': FixFieldDescriptor('TickDirection', 274, 'CHAR', str),
	'TimeInForce': FixFieldDescriptor('TimeInForce', 59, 'CHAR', str),
	'TotNoOrders': FixFieldDescriptor('TotNoOrders', 68, 'INT', int),
	'TotNoStrikes': FixFieldDescriptor('TotNoStrikes', 422, 'INT', int),
	'TotQuoteEntries': FixFieldDescriptor('TotQuoteEntries', 304, 'INT', int),
	'TotalNumSecurities': FixFieldDescriptor('TotalNumSecurities', 393, 'INT', int),
	'TotalVolumeTraded': FixFieldDescriptor('TotalVolumeTraded', 387, 'QTY', float),
	'TradSesCloseTime': FixFieldDescriptor('TradSesCloseTime', 344, 'UTCTIMESTAMP', str),
	'TradSesEndTime': FixFieldDescriptor('TradSesEndTime', 345, 'UTCTIMESTAMP', str),
	'TradSesMethod': FixFieldDescriptor('TradSesMethod', 338, 'INT', int),
	'TradSesMode': FixFieldDescriptor('TradSesMode', 339, 'INT', int),
	'TradSesOpenTime': FixFieldDescriptor('TradSesOpenTime', 342, 'UTCTIMESTAMP', str),
	'TradSesPreCloseTime': FixFieldDescriptor('TradSesPreCloseTime', 343, 'UTCTIMESTAMP', str),
	'TradSesReqID': FixFieldDescriptor('TradSesReqID', 335, 'STRING', str),
	'TradSesStartTime': FixFieldDescriptor('TradSesStartTime', 341, 'UTCTIMESTAMP', str),
	'TradSesStatus': FixFieldDescriptor('TradSesStatus', 340, 'INT', int),
	'TradeCondition': FixFieldDescriptor('TradeCondition', 277, 'MULTIPLEVALUESTRING', str),
	'TradeDate': FixFieldDescriptor('TradeDate', 75, 'LOCALMKTDATE', str),
	'TradeType': FixFieldDescriptor('TradeType', 418, 'CHAR', str),
	'TradingSessionID': FixFieldDescriptor('TradingSessionID', 336, 'STRING', str),
	'TransactTime': FixFieldDescriptor('TransactTime', 60, 'UTCTIMESTAMP', str),
	'URLLink': FixFieldDescriptor('URLLink', 149, 'STRING', str),
	'UnderlyingContractMultiplier': FixFieldDescriptor('UnderlyingContractMultiplier', 436, 'FLOAT', float),
	'UnderlyingCouponRate': FixFieldDescriptor('UnderlyingCouponRate', 435, 'FLOAT', float),
	'UnderlyingCurrency': FixFieldDescriptor('UnderlyingCurrency', 318, 'CURRENCY', str),
	'UnderlyingIDSource': FixFieldDescriptor('UnderlyingIDSource', 305, 'STRING', str),
	'UnderlyingIssuer': FixFieldDescriptor('UnderlyingIssuer', 306, 'STRING', str),
	'UnderlyingMaturityDay': FixFieldDescriptor('UnderlyingMaturityDay', 314, 'DAYOFMONTH', int),
	'UnderlyingMaturityMonthYear': FixFieldDescriptor('UnderlyingMaturityMonthYear', 313, 'MONTHYEAR', str),
	'UnderlyingOptAttribute': FixFieldDescriptor('UnderlyingOptAttribute', 317, 'CHAR', str),
	'UnderlyingPutOrCall': FixFieldDescriptor('UnderlyingPutOrCall', 315, 'INT', int),
	'UnderlyingSecurityDesc': FixFieldDescriptor('UnderlyingSecurityDesc', 307, 'STRING', str),
	'UnderlyingSecurityExchange': FixFieldDescriptor('UnderlyingSecurityExchange', 308, 'EXCHANGE', str),
	'UnderlyingSecurityID': FixFieldDescriptor('UnderlyingSecurityID', 309, 'STRING', str),
	'UnderlyingSecurityType': FixFieldDescriptor('UnderlyingSecurityType', 310, 'STRING', str),
	'UnderlyingStrikePrice': FixFieldDescriptor('UnderlyingStrikePrice', 316, 'PRICE', float),
	'UnderlyingSymbol': FixFieldDescriptor('UnderlyingSymbol', 311, 'STRING', str),
	'UnderlyingSymbolSfx': FixFieldDescriptor('UnderlyingSymbolSfx', 312, 'STRING', str),
	'UnsolicitedIndicator': FixFieldDescriptor('UnsolicitedIndicator', 325, 'BOOLEAN', str),
	'Urgency': FixFieldDescriptor('Urgency', 61, 'CHAR', str),
	'ValidUntilTime': FixFieldDescriptor('ValidUntilTime', 62, 'UTCTIMESTAMP', str),
	'ValueOfFutures': FixFieldDescriptor('ValueOfFutures', 408, 'AMT', float),
	'WaveNo': FixFieldDescriptor('WaveNo', 105, 'STRING', str),
	'WtAverageLiquidity': FixFieldDescriptor('WtAverageLiquidity', 410, 'FLOAT', float),
	'XmlData': FixFieldDescriptor('XmlData', 213, 'DATA', str),
	'XmlDataLen': FixFieldDescriptor('XmlDataLen', 212, 'INT', int),
}

_fix_message_types = {
	'Advertisement': ('7', True),
	'Allocation': ('J', True),
	'AllocationACK': ('P', True),
	'BidRequest': ('k', True),
	'BidResponse': ('l', True),
	'BusinessMessageReject': ('j', True),
	'DontKnowTrade': ('Q', True),
	'Email': ('C', True),
	'ExecutionReport': ('8', True),
	'Heartbeat': ('0', False),
	'IndicationofInterest': ('6', True),
	'ListCancelRequest': ('K', True),
	'ListExecute': ('L', True),
	'ListStatus': ('N', True),
	'ListStatusRequest': ('M', True),
	'ListStrikePrice': ('m', True),
	'Logon': ('A', False),
	'Logout': ('5', False),
	'MarketDataIncrementalRefresh': ('X', True),
	'MarketDataRequest': ('V', True),
	'MarketDataRequestReject': ('Y', True),
	'MarketDataSnapshotFullRefresh': ('W', True),
	'MassQuote': ('i', True),
	'NewOrderList': ('E', True),
	'NewOrderSingle': ('D', True),
	'News': ('B', True),
	'OrderCancelReject': ('9', True),
	'OrderCancelReplaceRequest': ('G', True),
	'OrderCancelRequest': ('F', True),
	'OrderStatusRequest': ('H', True),
	'Quote': ('S', True),
	'QuoteAcknowledgement': ('b', True),
	'QuoteCancel': ('Z', True),
	'QuoteRequest': ('R', True),
	'QuoteStatusRequest': ('a', True),
	'Reject': ('3', False),
	'ResendRequest': ('2', False),
	'SecurityDefinition': ('d', True),
	'SecurityDefinitionRequest': ('c', True),
	'SecurityStatus': ('f', True),
	'SecurityStatusRequest': ('e', True),
	'SequenceReset': ('4', False),
	'SettlementInstructions': ('T', True),
	'TestRequest': ('1', False),
	'TradingSessionStatus': ('h', True),
	'TradingSessionStatusRequest': ('g', True),
}

_fix_group_types = {
	'LinesOfText': [
		(58, 'Text'),
		(354, 'EncodedTextLen'),
		(355, 'EncodedText'),
		],
	'NoAllocs': [
		(79, 'AllocAccount'),
		(80, 'AllocShares'),
		],
	'NoBidComponents': [
		(12, 'Commission'),
		(13, 'CommType'),
		(66, 'ListID'),
		(421, 'Country'),
		(54, 'Side'),
		(44, 'Price'),
		(423, 'PriceType'),
		(406, 'FairValue'),
		(430, 'NetGrossInd'),
		(63, 'SettlmntTyp'),
		(64, 'FutSettDate'),
		(336, 'TradingSessionID'),
		(58, 'Text'),
		(354, 'EncodedTextLen'),
		(355, 'EncodedText'),
		],
	'NoBidDescriptors': [
		(399, 'BidDescriptorType'),
		(400, 'BidDescriptor'),
		(401, 'SideValueInd'),
		(404, 'LiquidityValue'),
		(441, 'LiquidityNumSecurities'),
		(402, 'LiquidityPctLow'),
		(403, 'LiquidityPctHigh'),
		(405, 'EFPTrackingError'),
		(406, 'FairValue'),
		(407, 'OutsideIndexPct'),
		(408, 'ValueOfFutures'),
		],
	'NoContraBrokers': [
		(375, 'ContraBroker'),
		(337, 'ContraTrader'),
		(437, 'ContraTradeQty'),
		(438, 'ContraTradeTime'),
		],
	'NoExecs': [
		(32, 'LastShares'),
		(17, 'ExecID'),
		(31, 'LastPx'),
		(29, 'LastCapacity'),
		],
	'NoIOIQualifiers': [
		(104, 'IOIQualifier'),
		],
	'NoMDEntries': [
		(279, 'MDUpdateAction'),
		(285, 'DeleteReason'),
		(269, 'MDEntryType'),
		(278, 'MDEntryID'),
		(280, 'MDEntryRefID'),
		(55, 'Symbol'),
		(65, 'SymbolSfx'),
		(48, 'SecurityID'),
		(22, 'IDSource'),
		(167, 'SecurityType'),
		(200, 'MaturityMonthYear'),
		(205, 'MaturityDay'),
		(201, 'PutOrCall'),
		(202, 'StrikePrice'),
		(206, 'OptAttribute'),
		(231, 'ContractMultiplier'),
		(223, 'CouponRate'),
		(207, 'SecurityExchange'),
		(106, 'Issuer'),
		(348, 'EncodedIssuerLen'),
		(349, 'EncodedIssuer'),
		(107, 'SecurityDesc'),
		(350, 'EncodedSecurityDescLen'),
		(351, 'EncodedSecurityDesc'),
		(291, 'FinancialStatus'),
		(292, 'CorporateAction'),
		(270, 'MDEntryPx'),
		(15, 'Currency'),
		(271, 'MDEntrySize'),
		(272, 'MDEntryDate'),
		(273, 'MDEntryTime'),
		(274, 'TickDirection'),
		(275, 'MDMkt'),
		(336, 'TradingSessionID'),
		(276, 'QuoteCondition'),
		(277, 'TradeCondition'),
		(282, 'MDEntryOriginator'),
		(283, 'LocationID'),
		(284, 'DeskID'),
		(286, 'OpenCloseSettleFlag'),
		(59, 'TimeInForce'),
		(432, 'ExpireDate'),
		(126, 'ExpireTime'),
		(110, 'MinQty'),
		(18, 'ExecInst'),
		(287, 'SellerDays'),
		(37, 'OrderID'),
		(299, 'QuoteEntryID'),
		(288, 'MDEntryBuyer'),
		(289, 'MDEntrySeller'),
		(346, 'NumberOfOrders'),
		(290, 'MDEntryPositionNo'),
		(387, 'TotalVolumeTraded'),
		(58, 'Text'),
		(354, 'EncodedTextLen'),
		(355, 'EncodedText'),
		],
	'NoMDEntryTypes': [
		(269, 'MDEntryType'),
		],
	'NoMiscFees': [
		(137, 'MiscFeeAmt'),
		(138, 'MiscFeeCurr'),
		(139, 'MiscFeeType'),
		],
	'NoMsgTypes': [
		(372, 'RefMsgType'),
		(385, 'MsgDirection'),
		],
	'NoOrders': [
		(11, 'ClOrdID'),
		(14, 'CumQty'),
		(39, 'OrdStatus'),
		(151, 'LeavesQty'),
		(84, 'CxlQty'),
		(6, 'AvgPx'),
		(103, 'OrdRejReason'),
		(58, 'Text'),
		(354, 'EncodedTextLen'),
		(355, 'EncodedText'),
		],
	'NoQuoteEntries': [
		(299, 'QuoteEntryID'),
		(55, 'Symbol'),
		(65, 'SymbolSfx'),
		(48, 'SecurityID'),
		(22, 'IDSource'),
		(167, 'SecurityType'),
		(200, 'MaturityMonthYear'),
		(205, 'MaturityDay'),
		(201, 'PutOrCall'),
		(202, 'StrikePrice'),
		(206, 'OptAttribute'),
		(231, 'ContractMultiplier'),
		(223, 'CouponRate'),
		(207, 'SecurityExchange'),
		(106, 'Issuer'),
		(348, 'EncodedIssuerLen'),
		(349, 'EncodedIssuer'),
		(107, 'SecurityDesc'),
		(350, 'EncodedSecurityDescLen'),
		(351, 'EncodedSecurityDesc'),
		(368, 'QuoteEntryRejectReason'),
		],
	'NoQuoteSets': [
		(302, 'QuoteSetID'),
		(311, 'UnderlyingSymbol'),
		(312, 'UnderlyingSymbolSfx'),
		(309, 'UnderlyingSecurityID'),
		(305, 'UnderlyingIDSource'),
		(310, 'UnderlyingSecurityType'),
		(313, 'UnderlyingMaturityMonthYear'),
		(314, 'UnderlyingMaturityDay'),
		(315, 'UnderlyingPutOrCall'),
		(316, 'UnderlyingStrikePrice'),
		(317, 'UnderlyingOptAttribute'),
		(436, 'UnderlyingContractMultiplier'),
		(435, 'UnderlyingCouponRate'),
		(308, 'UnderlyingSecurityExchange'),
		(306, 'UnderlyingIssuer'),
		(362, 'EncodedUnderlyingIssuerLen'),
		(363, 'EncodedUnderlyingIssuer'),
		(307, 'UnderlyingSecurityDesc'),
		(364, 'EncodedUnderlyingSecurityDescLen'),
		(365, 'EncodedUnderlyingSecurityDesc'),
		(304, 'TotQuoteEntries'),
		],
	'NoRelatedSym': [
		(311, 'UnderlyingSymbol'),
		(312, 'UnderlyingSymbolSfx'),
		(309, 'UnderlyingSecurityID'),
		(305, 'UnderlyingIDSource'),
		(310, 'UnderlyingSecurityType'),
		(313, 'UnderlyingMaturityMonthYear'),
		(314, 'UnderlyingMaturityDay'),
		(315, 'UnderlyingPutOrCall'),
		(316, 'UnderlyingStrikePrice'),
		(317, 'UnderlyingOptAttribute'),
		(436, 'UnderlyingContractMultiplier'),
		(435, 'UnderlyingCouponRate'),
		(308, 'UnderlyingSecurityExchange'),
		(306, 'UnderlyingIssuer'),
		(362, 'EncodedUnderlyingIssuerLen'),
		(363, 'EncodedUnderlyingIssuer'),
		(307, 'UnderlyingSecurityDesc'),
		(364, 'EncodedUnderlyingSecurityDescLen'),
		(365, 'EncodedUnderlyingSecurityDesc'),
		(319, 'RatioQty'),
		(54, 'Side'),
		(318, 'UnderlyingCurrency'),
		],
	'NoRoutingIDs': [
		(216, 'RoutingType'),
		(217, 'RoutingID'),
		],
	'NoStrikes': [
		(55, 'Symbol'),
		(65, 'SymbolSfx'),
		(48, 'SecurityID'),
		(22, 'IDSource'),
		(167, 'SecurityType'),
		(200, 'MaturityMonthYear'),
		(205, 'MaturityDay'),
		(201, 'PutOrCall'),
		(202, 'StrikePrice'),
		(206, 'OptAttribute'),
		(231, 'ContractMultiplier'),
		(223, 'CouponRate'),
		(207, 'SecurityExchange'),
		(106, 'Issuer'),
		(348, 'EncodedIssuerLen'),
		(349, 'EncodedIssuer'),
		(107, 'SecurityDesc'),
		(350, 'EncodedSecurityDescLen'),
		(351, 'EncodedSecurityDesc'),
		(140, 'PrevClosePx'),
		(11, 'ClOrdID'),
		(54, 'Side'),
		(44, 'Price'),
		(15, 'Currency'),
		(58, 'Text'),
		(354, 'EncodedTextLen'),
		(355, 'EncodedText'),
		],
	'NoTradingSessions': [
		(336, 'TradingSessionID'),
		],
}

_fix_field_numbers = {}
for desc in _fix_field_types.values():
	_fix_field_numbers[desc.number]=desc


_fix_group_numbers = {}
for name, desc in _fix_group_types.items():
	_fix_group_numbers[_fix_field_types[name].number]=desc


_fix_msgtype_table = {}
for name in _fix_message_types:
	_fix_msgtype_table[_fix_message_types[name][0]]=name


