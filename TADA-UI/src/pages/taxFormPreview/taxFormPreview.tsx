import React, { useEffect, useState } from 'react'
import { Breadcrumb, Collapse,Modal,Popconfirm, Table } from 'antd'
import { Link } from 'react-router-dom';
import { LoadingOutlined } from '@ant-design/icons';
import UserInfo from '../../components/userInfo/userInfo';
import Checkbox from '../../components/common/checkbox/checkbox';
import EditableTable from '../../components/editableGrid/editableGrid';
import commonConstants from '../../utils/constants/commonConstants';
import { isEmpty } from '../../utils/helper';
import { taxFormDataType, taxFormTableCellDataTyoe, taxFormTableConfigDataType, taxFormTableDataType } from '../taxForm/taxFormInterface';
import { useNavigate } from 'react-router-dom';

var _ = require('lodash')
const { Panel } = Collapse
const antIcon = (
    <LoadingOutlined
        style={{
            fontSize: 30,
        }}
        spin
    />
);
const TaxFormPreview = (props:any) => {
    const [taxData, setTaxData] = useState<taxFormDataType>();
    const[tableColumn,setTableColumn]=useState<any[]>();
    const [open, setOpen] = useState(false);
    const navigate = useNavigate();

    const convertArrayToObject = (array: taxFormTableDataType[], key: keyof taxFormTableCellDataTyoe) => {
         return array.map((eachdata: taxFormTableDataType) => {
            if(eachdata.columns !== undefined){
            return eachdata.columns.reduce(
                (obj, item) => ({
                    ...obj,
                    [item[key]]: item.columnValue
                }),
                { rowId: eachdata.rowId },
            ) 
            }
            else{
            
                    return eachdata
            }
        })
        
    }
    useEffect(() => {
        setTaxData(props.taxformAllData)
           const columns = props.taxformAllData.sections[0].tableConfig!.map((col: taxFormTableConfigDataType) => {
               if (!col.editable) {
                   return {...col,
                       dataIndex: col.key,
                       title: col.name,};
               }
               return {
                   ...col,
                   dataIndex: col.key,
                   title: col.name,
               };
           });
           const newColumns: any = [];
               columns.map((column: taxFormTableConfigDataType) => {
                   if (!isEmpty(column.groupName) && !isEmpty(column.groupDisplayText) && newColumns.filter((col: { title: string | undefined; }) => { return col.title == column.groupDisplayText }).length == 0) {
                       const tempHader = { 'title': column.groupDisplayText, 'groupName': column.groupName, 'children': columns.filter((eachcolumn: taxFormTableConfigDataType) => { return eachcolumn.groupName == column.groupName }) }
                       newColumns.push(tempHader)
                   }
                   else if (isEmpty(column.groupName)) {
                       newColumns.push(column)
                   }
               })
           setTableColumn(newColumns);
    }, [props.taxformAllData])
    
    // useEffect(() => {
    // if(props.isSubmitData == true){
    //     setOpen(true)
    // }
    // },[props.isSubmitData])

    const handleOk = () => {
        props.onSubmitButtonClick();
    };
    const handleCancel = () => {
        setOpen(false);
    };

    return (
        <div className="container content-wrapper">
            <div className="mb-2 row">
              
                <div className="col-md-12 p-0">{/*grid-margin*/}
                    <div className="d-flex mb-3  align-items-center">
                        <div className="col-8 pl-0 mt-3">
                            <h4 className="font-weight-bold mb-0">{`Tax Form  /   ${commonConstants.taxform.type} : ${props.state  && props.state.taxFormData && props.state.taxFormData.taxFormType}  /  ${commonConstants.taxform.year} : ${props.state && props.state.taxFormData&& props.state.taxFormData.year} `}</h4>
                        </div>
                        <div className="col-3 pl-0 mt-3">

                        </div>
                        <div className="col-3 pl-0 mt-3">

                        </div>
                    </div>
                </div>
                <div className="col-md-12 taxForm">
                    <UserInfo  />
                    
                        {taxData && taxData!.sections.map((eachSection) => {

                            return (
                                <div key={eachSection.sectionId}>
                                    <div className=" accordion__title mt-2 sectionHeader">
                                    {eachSection.sectionName  + " (" + eachSection.part + ")"}
                                  </div>
                                <div className='taxFormPanel' key={eachSection.sectionId}>
                                    <p data-test-id="description" className="taxFormDescription">{eachSection.description}</p>
                                    <hr />
                                    <p data-test-id="instruction" className='taxFormInstruction'>{eachSection.instruction}</p>
                                    <hr />
                                    <Checkbox config={eachSection.checkBoxConfig} data={eachSection.checkBoxData} updateFinalData={props.updateFinalData} sectionId={eachSection.sectionId} isDisabled={true}/>

                                        <div className="col-sm-12 mb-3">
                                        <div className="data-table-standard-container">
                                            <div className="table-responsive add-exchange-table">
                                            <Table
                                            data-testid="testTable"
                                               // scroll={{y:230}}
                                                columns={tableColumn}
                                                dataSource={convertArrayToObject((eachSection.tableData!),'columnId')}
                                                pagination={false} 
                                            // onChange={handleChangeTransactions}
                                            // pagination={pagination}
                                            />
                                            </div>
                                </div>
                            </div>

                                </div>
                                </div>
                                )
                        })}
  
                </div>
                {/* {taxData && taxData?.status == "Progressing" && */}
                <div className="col-md-12 d-flex pt-4">
                    <div  className="col-md-8"></div>
                        <div className="col-md-4 p-0" style={{margin:"6px"}}>
                        <button data-testid="save" className="float-right btn btn--progress btn--primary" 
                            title="Button"
                             onClick={()=> props.setOpenPreviewModal(false)}
                             > cancel</button>
                            <Popconfirm
                               placement="topRight"
                                title="This form Cannot be edited once Submitted.Are You sure you want to Submit this form?"
                                onConfirm={()=>{setOpen(true)}}
                                okText="Submit"
                                cancelText="Cancel"
                            > <button data-testid="submit" className="float-right btn btn--progress btn--primary" title="Button">Submit</button>
                            </Popconfirm>    
                                                
                        </div>
                    </div>
                {/* } */}
            </div>
            <Modal 
               // title="Title"
                visible={open}
                onOk={handleOk}
                onCancel={handleCancel}
            >
                <p>{"Data is saved successfully.Tax Form PDF will be generated in some time.Please visit the download documents page to download tax form."}</p>
            </Modal>
                </div>
    );
}
export default TaxFormPreview


