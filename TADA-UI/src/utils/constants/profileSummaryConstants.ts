
import DataTypeHoldings from "../../components/holdings/holdingsInterface";
import type { ColumnsType, SorterResult } from 'antd/lib/table/interface';

const holdingsColumns: ColumnsType<DataTypeHoldings> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => a.name.length - b.name.length,
      ellipsis: true,
      filterSearch: true,
      onFilter: (value: any, record) => record.name!.indexOf(value) === 0,
    },
    {
      title: 'Direction',
      dataIndex: 'direction',
      key: 'direction',
   // sorter: (a, b) => a.direction!.length - b.direction!.length,
    ellipsis: true,
    filterSearch: false,
     // onFilter: (value: any, record) => record.direction!.indexOf(value) === 0,
    },
    {
      title: 'Amount',
      dataIndex: 'amount',
      key: 'amount',
      sorter: (a, b) => a.amount - b.amount,
      ellipsis: true,
      filterSearch: true,
      onFilter: (value: any, record) => record.amount == value,
    },
    {
      title: 'Total Value',
      dataIndex: 'totalValue',
      key: 'totalValue',
      sorter: (a, b) => a.totalValue - b.totalValue,
      ellipsis: true,
      filterSearch: true,
      onFilter: (value: any, record) => record.totalValue === value,
    },
  ];

  const taxValues = 
    {
       ltcg: 20,
       portfolioValueIn:34567,
       portfolioValueOut:2000,
       stcg:95.34567,
       taxLiability:95.34567
    }

const holdingsData=
[
  {"name":"KODA","amount":5,"totalValue":1000,"direction":"in","iconName":""},
  {"name":"EMYTH","amount":1,"totalValue":86.58,"direction":"in","iconName":""},
  {"name":"LAG","amount":1,"totalValue":83.87,"direction":"in","iconName":""},
  {"name":"ETH","amount":3.3936084400000004,"totalValue":566.7456758211999,"direction":"in","iconName":""},
  {"name":"SPH3RES","amount":1,"totalValue":232.85,"direction":"in","iconName":""},

]

export default { holdingsColumns,taxValues,holdingsData}
