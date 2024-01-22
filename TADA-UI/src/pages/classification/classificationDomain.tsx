import { classificationDataType, EditableRowProps, EditableCellProps, ClassificationDataResponse, ClassificationSaveResponse } from './classifcationInterface'
import type {
  TablePaginationConfig,
} from 'antd/lib/table/interface'
import moment from 'moment';
import React, { useEffect, useState, useRef, useContext } from 'react'
import { DatePicker, InputNumber, message, Popconfirm, Select, TableProps } from 'antd'
import { useMsal } from '@azure/msal-react'
import ClassficationService from '../../services/api/classificationService'
import ClassificationConstants from '../../utils/constants/classificationConstants'
import { useNavigate } from 'react-router-dom'
import { ColumnFilterItem } from 'antd/lib/table/interface'
import commonConstants from '../../utils/constants/commonConstants';
import { useSelector } from 'react-redux'
import { profileStore } from '../../utils/store/store'
import { getRndIntegerBetWeen, isEmpty, numberIntoCurrency, setImagePath, useInterval } from '../../utils/helper'
import { Form, Input } from 'antd'
import type { InputRef } from 'antd';
import type { FormInstance } from 'antd/es/form';
import Logger from '../../services/azure/appInsights/Logger/logger'
import { SeverityLevel } from '@microsoft/applicationinsights-web'
import messages from '../../utils/constants/messages'
import { EditOutlined } from '@ant-design/icons'

const ClassficationDomain = () => {
  let { instance, accounts } = useMsal()
  const currentProfile = useSelector(profileStore);
  const [loader, setLoader] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState<string>("")
  const navigate = useNavigate()
  const [isClassificationCompleted, SetIsClassificationCompleted] = useState(false);
  const [classification, setClassification] = useState();
  const [classificationData, setClassificationData] = useState<
    classificationDataType[]
  >([])
  const [form] = Form.useForm();
  const [editingKey, setEditingKey] = useState('');

  const [pagination, setPagination] = useState<TablePaginationConfig>({
    current: 1,
    pageSize: 5,
    pageSizeOptions: commonConstants.paginationOptions,
    showSizeChanger: true
  })
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
  const handleChangeTransactions: TableProps<
    classificationDataType
  >['onChange'] = (newPagination) => {
    setPagination({ ...newPagination })
  }

  const onSelectChange = (
    newSelectedRowKeys: React.Key[], selectedRows: classificationDataType[]
  ) => {
    setSelectedRowKeys([...newSelectedRowKeys])
  }
  const rowSelection = {
    selectedRowKeys,
    onChange: onSelectChange,
  }
  useInterval(() => {
    getClassificationStatus();
  }, isClassificationCompleted ? null : (getRndIntegerBetWeen(5, 10) * 1000));

  useEffect(() => {
    getClassificationStatus();
  }, [])


  const setActionColumns = () => {
    classificationColumns.map((eachColumn: {
      editable: any; dataIndex: any; title: any; key: string; filters: ColumnFilterItem[];
      render: { (text: string, row: any): JSX.Element; (text: string, row: any): JSX.Element }
    }) => {
      if (eachColumn.key == commonConstants.columnName.Action) {
        eachColumn.render = (_: any, record: classificationDataType) => {
          const editable = isEditing(record);
          return editable ? (
            <span>
              <Popconfirm title="Are you sure want to Save?" onConfirm={() => handleSave(record.id)}>
                <button className="action-icons" >
                  <i className="material-icons menu-icon" >save</i></button>
              </Popconfirm>      <Popconfirm title="Sure to cancel?" onConfirm={cancelEdit}>
                <button className="action-icons" >
                  <i className="material-icons menu-icon red pl-4" >cancel</i></button>
              </Popconfirm>


            </span>
          ) : (
            <button className="action-icons" disabled={!isEmpty(editingKey)} onClick={() => editRow(record)}> <i className="material-icons menu-icon pl-2">edit</i></button>
          );
        }
      }
    });
  }
  const getClassificationStatus = () => {
    Logger.trackTrace({
      message: 'getting classification status',
      data: `id =${String(currentProfile.clientId)}`,
      severityLevel: SeverityLevel.Information,
    })
    ClassficationService.getClassificationStatus(instance, accounts, currentProfile.clientId!).then(
      (response: { status: string, message: string }) => {
        if (!isEmpty(response)) {
          Logger.trackTrace({
            message: 'returned  classification status',
            data: `id =${JSON.stringify(response)}`,
            severityLevel: SeverityLevel.Information,
          })
          if (response.status == "completed" || response.status == "Not Started") {
            SetIsClassificationCompleted(true);
            getClassificationData();
          }
          else if (response.status == "fail") {
            message.error(messages.classificationStatusError)
            SetIsClassificationCompleted(true);
            getClassificationData();
          }

        }
      }).catch((err) => {
        //remove this line once api started working
        SetIsClassificationCompleted(true);
        getClassificationData();
        Logger.trackTrace({
          message: 'error in getting classification status',
          data: `id =${String(currentProfile.clientId)}`,
          severityLevel: SeverityLevel.Information,
        })
        Logger.trackException({ message: err })
        message.error(messages.classificationStatusError)
        SetIsClassificationCompleted(true);
      })
  }
  let getClassificationData = () => {
    setLoader(true);
    setLoadingMessage(messages.gettingUnClassificationData);
    Logger.trackTrace({
      message: 'getting classification data',
      data: `id =${String(currentProfile.clientId)}`,
      severityLevel: SeverityLevel.Information,
    })
    getClassificationDataByPagination(0, 500);

  }
  let classificData: any[] = [];
  const getClassificationDataByPagination = (start: number, end: number) => {
    ClassficationService.getClassificationData(instance, accounts, currentProfile.clientId!, start, end).then(
      (response: ClassificationDataResponse) => {
        if (response != null) {
          classificData.push(...response.data);
          setClassificationData((prevState) => [...prevState, ...response.data])
          if (response.data.length == end) {
            getClassificationDataByPagination(start + end, end)
          }
          else {
            setLoader(false);
            setFilters(classificData);
            //  setPagination({...pagination,total:classificationData.length})

          }
        }
      }).catch((err) => {
        setLoader(false);
      })
  }
  const classificationColumns = ClassificationConstants.classificationColumns;
  setActionColumns();
  function setFilters(response: classificationDataType[]) {
    classificationColumns.map((eachColumn: {
      editable: any; dataIndex: any; title: any; key: string; filters: ColumnFilterItem[];
      render: { (text: string, row: any): JSX.Element; (text: string, row: any): JSX.Element }
    }) => {

      let currentSet: Set<string> = new Set(response.map((data) => String(data[eachColumn.key as keyof classificationDataType])))
      let filterObj: ColumnFilterItem[] = [];
      currentSet.forEach((item: string) => {
        filterObj.push({
          text: item,
          value: item,
        })
      });
      eachColumn.filters = [...filterObj];

    })
  }
  const EditableCell: React.FC<EditableCellProps> = ({
    editable,
    editing,
    dataIndex,
    title,
    inputType,
    record,
    children,
    ...restProps
  }) => {

    return (
      <td {...restProps}>
        {editing ? (
          <Form.Item
            name={dataIndex}
            shouldUpdate
            style={{ margin: 0 }}
            rules={[
              {
                required: true,
                message: `${title}*`,
              },
            ]}
          >
            <>
              {inputType === "date" && <DatePicker defaultValue={moment(record[dataIndex],)}
                onChange={(date, dateString) => {
                  form.setFieldsValue({ [dataIndex]: dateString })
                }} />}
              {inputType == "text" && <Input defaultValue={record[dataIndex]} onChange={(e) => {
                form.setFieldsValue({ [dataIndex]: e.target.value })
              }} />}
              {inputType == "number" && <InputNumber defaultValue={record[dataIndex]} onChange={(value) => {
                form.setFieldsValue({ [dataIndex]:value })
              }} />}
              {inputType == "select" && <Select
                showSearch
                placeholder=""
                onChange={(value) => { form.setFieldsValue({ [dataIndex]: value }) }} options={ClassificationOptions}
                allowClear
                className=""
                defaultValue={record[dataIndex]}>
              </Select>}
            </>
          </Form.Item>
        ) : (
          children
        )}
      </td>
    );
  };
  const isEditing = (record: classificationDataType) => {
    return record.id.toString() == editingKey;
  }
  const editRow = (record: Partial<classificationDataType> & { key: React.Key }) => {
    form.setFieldsValue({
      TxDirection: "", wallet: "",
      TxHash: "",
      From: "",
      To: "",
      Token: "",
      TransactionDesc: "",
      Amount: "",
      Price: "",
      id: "",
      TimeStamp: new Date(), ...record
    });
    setEditingKey(record.id!.toString());
  };

  const cancelEdit = () => {
    setEditingKey('');
  };

  const handleSave = async (key: React.Key) => {

    try {
      const row = await form.validateFields() as classificationDataType;

      form.validateFields().then(function (res) {
        console.log(res)
      });
      const newData = [...classificationData];
      const index = newData.findIndex(item => key === item.id);
      if (index > -1) {
        const item = newData[index];
        newData.splice(index, 1, {
          ...item,
          ...row,
        });
        setClassificationData(newData);
        row.id = item.id;
        saveClassifiedData(row)
        setEditingKey('');
      } else {
        newData.push(row);
        setClassificationData(newData);
        setEditingKey('');
      }
    } catch (errInfo) {
      console.log('Validate Failed:', errInfo);
    }
  };


  const ClassificationOptions = ClassificationConstants.ClassificationOptions

  const onClassificationChange = (value: any) => {
    setClassification(value);
    var tempOldClassificationData = [...classificationData]
    tempOldClassificationData.forEach((eachData, key) => {
      if (
        selectedRowKeys.filter((selectedRow) => {
          return selectedRow == eachData.id
        }).length > 0
      ) {
        eachData.TxDirection = value
        tempOldClassificationData[key] = {
          ...tempOldClassificationData[key],
          TxDirection: value,
        }
      }
    })
    setClassificationData([...tempOldClassificationData])
  }

  const saveClassifiedData = (currentClassifiedData: classificationDataType) => {
    setLoader(true);
    setLoadingMessage(messages.savingUnclassifiedData);
    Logger.trackTrace({
      message: 'saving classification data',
      data: `data =${JSON.stringify(classificationData)}`,
      severityLevel: SeverityLevel.Information,
    })
    ClassficationService.saveClassifiedData(instance, accounts, currentProfile.clientId!, currentClassifiedData)
      .then((response: ClassificationSaveResponse) => {
        if (isEmpty(response.error) && !isEmpty(response.id)) {
          setLoader(false);
          setClassificationData(current =>
            current.filter(element => {
              return element.id !== response.id;
            })
          )
          Logger.trackTrace({
            message: 'retruned response of saving classification data',
            data: `data =${JSON.stringify(response)}`,
            severityLevel: SeverityLevel.Information,
          })
        }
      }).catch((err) => {
        setLoader(false);
        Logger.trackTrace({
          message: 'error in saving classification data',
          data: `id =${JSON.stringify(classificationData)}`,
          severityLevel: SeverityLevel.Information,
        })
        Logger.trackException({ message: err })
        message.error(messages.errorSavingUnclassifiedData)
      })
  }

  return {
    isClassificationCompleted,
    classification,
    handleChangeTransactions,
    classificationData,
    classificationColumns,
    rowSelection,
    onClassificationChange,
    ClassificationOptions,

    pagination,
    loader,
    loadingMessage,
    form,
    EditableCell,
    isEditing
  }
}
export default ClassficationDomain
