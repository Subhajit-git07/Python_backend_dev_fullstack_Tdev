interface classificationDataType {
  Wallet: number,
  TxHash: number,
  From: number,
  To: number,
  Token: string,
  TransactionDesc: string,
  TxDirection: string,
  Amount: string,
  Price: string,
  key: string,
  id: string,
}
interface ClassificationSaveResponse{
  Wallet: number,
  TxHash: number,
  From: number,
  To: number,
  Token: string,
  TransactionDesc: string,
  TxDirection: string,
  Amount: string,
  Price: string,
  key: string,
  id: string,
  error?:{}
}
interface ClassificationOptionType {
  name: string,
  value: string
}
interface ClassificationDataResponse {
  page: number,
  page_size: number,
  count: number,
  data: classificationDataType[],

}
interface EditableRowProps {
  index: number;
}
interface EditableCellProps {
  title: React.ReactNode;
  editable: boolean;
  editing: boolean;
  inputType: 'number' | 'text' | 'date' | 'select',
  children: React.ReactNode;
  dataIndex: keyof classificationDataType;
  record: classificationDataType;
  handleSave: (record: classificationDataType) => void;
}

export type { classificationDataType,ClassificationSaveResponse, ClassificationOptionType, EditableRowProps, EditableCellProps, ClassificationDataResponse }