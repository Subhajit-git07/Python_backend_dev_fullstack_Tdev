export interface taxFormConfigDataType {
  formType: string,
  year: string,
  status: string,
  sections: {
    sectionName: string,
    sectionId: string,
    description: string,
    part: string,
    instruction: string,
    checkBoxConfig: taxFormCheckBoxConfigDataType[],
    tableConfig: taxFormTableConfigDataType[]
  }[]
}

export interface taxFormCheckBoxConfigDataType {
  optionId: string,
  displayText: string,
  defaultValue: boolean
}

export interface taxFormTableConfigDataType {
  key: string,
  name: string,
  columnId: string,
  regex: string,
  inputType: "text" | "date" | "number" | "Multiline" | "select",
  defaultValue?: string,
  options?: string[],
  groupName?: string,
  groupDisplayText?: string,
  editable: boolean,
  isRequired: boolean,
  children?: taxFormTableConfigDataType[],
  render?: (value: string) => {}
}

export interface taxFormTableDataType {
  rowId: string,
  columns: taxFormTableCellDataTyoe[],
}
export interface taxFormTableCellDataTyoe {
  columnId: string,
  columnValue: string,
  cellId: string,
}
export interface taxFormStateDataType {
 
    year?: string,
    taxFormType?: string

}

export interface taxFormDataType {
  status: string,
  sections: {
    sectionName: string,
    sectionId: string,
    description: string,
    part: string,
    instruction: string,
    checkBoxConfig?: taxFormCheckBoxConfigDataType[],
    tableConfig?: taxFormTableConfigDataType[]
    checkBoxData?: taxformCheckboxDatatType[],
    tableData?: taxFormTableDataType[],
    tableDataLoaded?: boolean,
  }[]
}
export interface taxformTableDataResponseType {
  sectionId: string,
  tableData?: taxFormTableDataType[]
}

export interface taxformCheckboxDatatType {
  name: string, optionValue: boolean, optionId: string
}




