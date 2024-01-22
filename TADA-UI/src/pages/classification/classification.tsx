import React from 'react'
import { Breadcrumb, Form, Select, Table } from 'antd'
import classificationDomain from './classificationDomain';
import { Link } from 'react-router-dom';
import { isEmpty } from '../../utils/helper';
import { LoadingOutlined } from '@ant-design/icons';
import { Spin } from 'antd';
import LoadingOverlay from 'react-loading-overlay-ts';
import messages from '../../utils/constants/messages';
import { classificationDataType } from './classifcationInterface';

const antIcon = (
    <LoadingOutlined
        style={{
            fontSize: 30,
        }}
        spin
    />
);
const Classfication = () => {

    const { isClassificationCompleted, classification, handleChangeTransactions, classificationData, classificationColumns, rowSelection,
        onClassificationChange, ClassificationOptions, pagination, loader,loadingMessage,form, EditableCell, isEditing } = classificationDomain();

    const columns = classificationColumns.map((col: { key: string, editable: any; dataIndex: any; title: any;inputType:string }) => {

        if (!col.editable) {
            return col;
        }
        return {
            ...col,
            onCell: (record: classificationDataType) => ({
                record,
                editable: col.editable,
                dataIndex: col.dataIndex,
                inputType: col.inputType,
                title: col.key,
                editing: isEditing(record),
            })
        };
    });

    const components = {
        body: {
            cell: EditableCell
        }
    };

    return (
        <LoadingOverlay
            active={loader || !isClassificationCompleted} 
            spinner={<Spin tip={!isClassificationCompleted ? messages.classificationStillInProgress : loadingMessage}
                indicator={antIcon}
                style={{ color: "#FFE600", whiteSpace: 'pre-line' }}
            />}
        >
            <div className="container content-wrapper">
                <div className="mb-2 row">
                    <div className="col-12 p-0 align-items-center">
                        <div aria-label="Breadcrumb" className="d-flex breadcrumb-item ">
                            <Breadcrumb separator="›" aria-label="breadcrumb">
                                <Breadcrumb.Item> <Link color="inherit" to="/TADA/profileSummary">
                                    Profile Summary
                                </Link></Breadcrumb.Item>
                                <Breadcrumb.Item> <Link color="inherit" to="/TADA/addtransactions/wallet">
                                    Add Transaction
                                </Link></Breadcrumb.Item>
                                <Breadcrumb.Item> Classification</Breadcrumb.Item>
                            </Breadcrumb>
                        </div>
                    </div>
                    <div className="col-md-12 p-0">{/*grid-margin*/}
                        <div className="d-flex mb-3  align-items-center">
                            <div className="col-8 pl-0 mt-3">
                                <h4 className="font-weight-bold mb-0">Manual Classification</h4>
                            </div>

                        </div>
                    </div>
                    <div className="card mt-3">
                        <div className="card-body">

                            <div className="row">
                                <div className="col-sm-12">
                                    <div className="data-table-standard-container">
                                        <div className="table-responsive">
                                            <Form form={form} component={false}>
                                                <Table
                                                    components={components}
                                                    pagination={pagination}
                                                    rowSelection={rowSelection}
                                                    data-testid="classificationData"
                                                    rowKey="id"
                                                    scroll={{ x: '100%' }}
                                                    columns={columns}
                                                    dataSource={classificationData}
                                                    onChange={handleChangeTransactions} />
                                            </Form>
                                        </div>
                                    </div>

                                </div>

                                <div className="col-12 d-flex">
                                    <div className="col-4">
                                        <Link to="/TADA/profileSummary"> 
                                               <button data-testid="back" className="  btn btn--progress btn--progress-secondary" title="Button">Back</button></Link>
                                    </div>
                                    <div className=" col-8 va-middle">
                                        <div className="float-right dropdown dropdown--single-select">

                                            <Select
                                                showSearch
                                                placeholder=""
                                                onChange={onClassificationChange} options={ClassificationOptions}
                                                allowClear
                                                data-testid="transactiondirection"
                                                className="dropdown-toggle big-dropdown" >
                                            </Select>
                                            <label className={`textinput-group__label ${(!isEmpty(classification)) ? 'focus' : ''}`} htmlFor="text-input-default2">Transaction Direction</label>

                                        </div>
                                        <button data-testid="classify" className="float-right btn btn--progress btn--primary" title="Button"> Classify</button>


                                    </div>


                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </LoadingOverlay>
    );
}
export default Classfication


