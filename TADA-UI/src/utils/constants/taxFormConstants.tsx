import { DefaultSerializer } from 'v8';
import checkboxInterface from '../../components/common/checkbox/checkboxInterface';
import { taxFormConfigDataType, taxFormTableDataType,taxFormDataType, taxformTableDataResponseType } from '../../pages/taxForm/taxFormInterface';

const taxFormconfig: taxFormConfigDataType = {
  formType: "8949",
  year: "2022",
  status:"Progressing",
  sections: [{
    sectionName: "Short Term Captial Gain", 
    sectionId: "82c00424-69a9-49a2-a400-da700453c2b0",
    description: 'Before you check Box A, B, or C below, see whether you received any Form(s) 1099-B or substitute statement(s) from your broker. A substitute statement will have the same information as Form 1099-B. Either will show whether your basis (usually your cost) was reported to the IRS by your broker and may even tell you which box to check',
    part:'Part1',
    instruction:'You must check Box A, B, or C below. Check only one box. If more than one box applies for your short-term transactions, complete a separate Form 8949, page 1, for each applicable box. If you have more short-term transactions than will fit on this page for one or more of the boxes, complete as many forms with the same box checked as you need.',
    checkBoxConfig: [
      { optionId: 'optionA', displayText: '(A) Short-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS (see Note above)', defaultValue: false },
      { optionId: 'optionB', displayText: '(B) Short-term transactions reported on Form(s) 1099-B showing basis wasn’t reported to the IRS', defaultValue: false },
      { optionId: 'optionC', displayText: '(C) Short-term transactions not reported to you on Form 1099-B', defaultValue: false },

    ],
    tableConfig: [
      {
        key: "description",
        name: "(a) \n Description of property \n Example: 100 sh. XYZ Co.)",
        columnId: "531d59e8-bdb5-4768-8096-893cceb450a2",
        regex: "",
        inputType: "Multiline",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: true
      },
      {
        key: "dateAcuired",
        name: "(b) \n Date acquired \n (Mo., day, yr.)",
        columnId: "c197055b-df62-4aeb-9448-b142460b6800",
        regex: "",
        inputType: "date",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "dateSold",
        name: "(c) \n Date sold or\n disposed of \n (Mo., day, yr.)",
        columnId: "bc2d3b62-9a58-4336-84fe-c132be08fac9",
        regex: "",
        inputType: "date",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "proceeds",
        name: "(d) \n Proceeds \n (sales price) \n (see instructions)",
        columnId: "ffdad995-e661-4763-a601-8a0bd9ca21aa",
        regex: "",
        inputType: "number",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: true
      },
      {
        key: "otherBasics",
        name: "(e) \n Cost or other basis. \n See the Note below \n and see Column (e) \n in the separate \n instructions",
        columnId: "29d999a3-afd5-4d31-a9bd-a17641940889",
        regex: "",
        inputType: "number",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "codeInstructions",
        name: "(f) \n Code(s) from \n instructions",
        columnId: "a3e1a758-79c7-4efc-af81-81a96b9d9317",
        regex: "",
        inputType: "select",
        options: ['optionA','optionB'],
        groupName: "adjustment",
        groupDisplayText: "Adjustment, if any, to gain or loss. \n If you enter an amount in column (g), \n enter a code in column (f). \n See the separate instructions",
        editable: true,
        isRequired: false
      },
      {
        key: "amountOfAdjustment",
        name: "(g) \n Amount of \n adjustment",
        columnId: "0d23c374-71ad-48ba-9ef0-46f149680b9f",
        regex: "",
        inputType: "number",
        options: [],
        groupName: "adjustment",
        groupDisplayText: "Adjustment, if any, to gain or loss. \n If you enter an amount in column (g), \n enter a code in column (f). \n See the separate instructions",
        editable: true,
        isRequired: false
      },
      {
        key: "gainOrLoss",
        name: "(h) \n Gain or (loss). \n Subtract column (e) \n from column (d) and \n combine the result \n with column (g)",
        columnId: "149c49f4-6526-42a9-a53a-c7dc1abfe98f",
        regex: "^[0-9]+$",
        inputType: "text",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
    ]
  },
  {
    sectionName: "Long Term Captial Gain",
    sectionId: "8b909d8b-4308-4de0-b62b-77f5a62f26a5",
    description: 'Before you check Box D, E, or F below, see whether you received any Form(s) 1099-B or substitute statement(s) from your broker. A substitute     statement will have the same information as Form 1099-B. Either will show whether your basis (usually your cost) was reported to the IRS by your    broker and may even tell you which box to check',
    part:'Part2',
    instruction:'You must check Box D, E, or F below. Check only one box. If more than one box applies for your long-term transactions, complete a separate Form 8949, page 2, for each applicable box. If you have more long-term transactions than will fit on this page for one or more of the boxes, complete as many forms with the same box checked as you need.',
    checkBoxConfig: [
      { optionId: 'optionD', displayText: '(D) Long-term transactions reported on Form(s) 1099-B showing basis was reported to the IRS (see Note above)', defaultValue: false },
      { optionId: 'optionE', displayText: '(E) Long-term transactions reported on Form(s) 1099-B showing basis wasn’t reported to the IRS', defaultValue: false },
      { optionId: 'optionF', displayText: '(F) Long-term transactions not reported to you on Form 1099-B', defaultValue: false },

    ],
    tableConfig: [
      {
        key: "description",
        name: "(a) \n Description of property \n Example: 100 sh. XYZ Co.)",
        columnId: "531d59e8-bdb5-4768-8096-893cceb450a2",
        regex: "",
        inputType: "Multiline",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "dateAcuired",
        name: "(b) \n Date acquired \n (Mo., day, yr.)",
        columnId: "c197055b-df62-4aeb-9448-b142460b6800",
        regex: "",
        inputType: "date",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "dateSold",
        name: "(c) \n Date sold or\n disposed of \n (Mo., day, yr.)",
        columnId: "bc2d3b62-9a58-4336-84fe-c132be08fac9",
        regex: "",
        inputType: "date",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "proceeds",
        name: "(d) \n Proceeds \n (sales price) \n (see instructions)",
        columnId: "ffdad995-e661-4763-a601-8a0bd9ca21aa",
        regex: "",
        inputType: "number",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "otherBasics",
        name: "(e) \n Cost or other basis. \n See the Note below \n and see Column (e) \n in the separate \n instructions",
        columnId: "29d999a3-afd5-4d31-a9bd-a17641940889",
        regex: "",
        inputType: "number",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: true,
        isRequired: false
      },
      {
        key: "codeInstructions",
        name: "(f) \n Code(s) from \n instructions",
        columnId: "a3e1a758-79c7-4efc-af81-81a96b9d9317",
        regex: "",
        inputType: "text",
        options: [],
        groupName: "adjustment",
        groupDisplayText: "Adjustment, if any, to gain or loss. \n If you enter an amount in column (g), \n enter a code in column (f). \n See the separate instructions",
        editable: true,
        isRequired: false
      },
      {
        key: "amountOfAdjustment",
        name: "(g) \n Amount of \n adjustment",
        columnId: "0d23c374-71ad-48ba-9ef0-46f149680b9f",
        regex: "",
        inputType: "select",
        options: ['optionA','optionB'],
        groupName: "adjustment",
        groupDisplayText: "Adjustment, if any, to gain or loss. \n If you enter an amount in column (g), \n enter a code in column (f). \n See the separate instructions",
        editable: true,
        isRequired: false
      },
      {
        key: "gainOrLoss",
        name: "(h) \n Gain or (loss). \n Subtract column (e) \n from column (d) and \n combine the result \n with column (g)",
        columnId: "149c49f4-6526-42a9-a53a-c7dc1abfe98f",
        regex: "",
        inputType: "text",
        options: [],
        groupName: "",
        groupDisplayText: "",
        editable: false,
        isRequired: false
      },
    ]
  }
  ]
}

const checkboxData:taxFormDataType={
  status:"Progressing",
  sections: [{
    sectionName: "Short Term Captial Gain",
    sectionId: "82c00424-69a9-49a2-a400-da700453c2b0",
    description: 'Before you check Box A, B, or C below, see whether you received any Form(s) 1099-B or substitute statement(s) from your broker. A substitute     statement will have the same information as Form 1099-B. Either will show whether your basis (usually your cost) was reported to the IRS by your     broker and may even tell you which box to check',
    part:'Part1',
    instruction:'You must check Box A, B, or C below. Check only one box. If more than one box applies for your short-term transactions, complete a separate Form 8949, page 1, for each applicable box. If you have more short-term transactions than will fit on this page for one or more of the boxes, complete as many forms with the same box checked as you need.',
    checkBoxData: [
      { name: 'optionA', optionValue: true, optionId:"12345"},
      { name: 'optionB', optionValue: false, optionId:"12346" },
      { name: 'optionC', optionValue: true, optionId:"12347"},
    ]
},
{
  sectionName: "Long Term Captial Gain",
  sectionId: "8b909d8b-4308-4de0-b62b-77f5a62f26a5",
  description: 'Before you check Box D, E, or F below, see whether you received any Form(s) 1099-B or substitute statement(s) from your broker. A substitute     statement will have the same information as Form 1099-B. Either will show whether your basis (usually your cost) was reported to the IRS by your    broker and may even tell you which box to check',
  part:'Part2',
    instruction:'You must check Box D, E, or F below. Check only one box. If more than one box applies for your long-term transactions, complete a separate Form 8949, page 2, for each applicable box. If you have more long-term transactions than will fit on this page for one or more of the boxes, complete as many forms with the same box checked as you need.',
  checkBoxData: [
    { name: 'optionD', optionValue: true, optionId:"12348" },
    { name: 'optionE', optionValue: false, optionId:"12345" },
    { name: 'optionF', optionValue: false, optionId:"12345" },

  ],

}]
}

const shortTermTableData:taxformTableDataResponseType={
  sectionId:"82c00424-69a9-49a2-a400-da700453c2b0",
  tableData:[
    {
  rowId: "d780420f-368c-4fbf-bcac-eff27e94b7a4",
  columns:[
  {
    columnId: "description",
    columnValue: "100.00 Aglient Technologies Inc (A)",
    cellId: "6907d021-1b73-4f41-8f37-26ec1f5c14bc",
  },
  {
    columnId: "dateAcuired",
    columnValue: "2021-09-13 12:55:34",
    cellId: "e2fef9ae-51c4-449d-9b41-26e8e0fca3ff",
  },
  {
    columnId: "dateSold",
    columnValue: "2022-03-23 02:45:39",
    cellId: "38a5741b-4426-47b4-bf72-9e24428e0a55",
  },
  {
    columnId: "proceeds",
    columnValue: "150000",
    cellId: "26e6bdaa-af6e-4b06-a541-650893930247",
  },
  {
    columnId: "otherBasics",
    columnValue: "220000",
    cellId: "499778a8-b30f-49ef-800e-8e30367baf37",
  },
  {
    columnId: "codeInstructions",
    columnValue: "W",
    cellId: "d9f64aec-40d6-4a26-a613-7671e8c78cd4",
  },
  {
    columnId: "amountOfAdjustment",
    columnValue: "500.00",
    cellId: "af17fefe-70cf-485a-9310-7ba4bb4df70f",
  },
  {
    columnId: "gainOrLoss",
    columnValue: "0.00",
    cellId: "6907d021-1b73-4f41-8f37-26ec1f5c14bc",
  },
],
},
{
  rowId: "50938017-5c2c-426c-9cea-9de6ee2991e8",
  columns:[
  {
    columnId: "description",
    columnValue: "10.00 Corp Action G/L ADN Corp(AQN)",
    cellId: "f1636f08-2a79-4479-8476-e648e7e1cf30",
  },
  {
    columnId: "dateAcuired",
    columnValue: "2021-09-13 12:55:34",
    cellId: "0665adb1-7c91-4c0f-af1b-b1dd0a990928",
  },
  {
    columnId: "dateSold",
    columnValue: "2022-03-23 02:45:39",
    cellId: "7495d204-5e27-4329-bc4e-a0d079bb3b34",
  },
  {
    columnId: "proceeds",
    columnValue: "490.98",
    cellId: "ddd27144-1b67-4fc3-aede-5c68edcc849d",
  },
  {
    columnId: "otherBasics",
    columnValue: "100.00",
    cellId: "cdf049da-6b0b-46db-8135-19f61576d4d2",
  },
  {
    columnId: "codeInstructions",
    columnValue: "",
    cellId: "87a2801a-714c-48c6-b847-5c3f862a2fa9",
  },
  {
    columnId: "amountOfAdjustment",
    columnValue: "",
    cellId: "f8ad9fff-a75a-4fd4-bc4b-4f1eeafaa59e",
  },
  {
    columnId: "gainOrLoss",
    columnValue: "390.48",
    cellId: "70166f1b-52d6-4fdc-8eb2-2b65d2f17840",
  },
],
}
]}

const longTermTableData:taxformTableDataResponseType={
  sectionId:"8b909d8b-4308-4de0-b62b-77f5a62f26a5",
  tableData:[
    {
  rowId: "d38f1bc8-c50e-47e5-9909-7d2c2516d467",
  columns:[
  {
    columnId: "description",
    columnValue: "L 100.00 Aglient Technologies Inc (A)",
    cellId: "ccf94c74-1436-4c01-92e8-d9ddafdb1f5f",
  },
  {
    columnId: "dateAcuired",
    columnValue: "2021-09-13 12:55:34",
    cellId: "f028264a-58c5-4ed4-ac4a-06c475ac54a6",
  },
  {
    columnId: "dateSold",
    columnValue: "2022-03-23 02:45:39",
    cellId: "2e5e5755-8b3b-4a7e-b143-6df46f51f7dc",
  },
  {
    columnId: "proceeds",
    columnValue: "150000",
    cellId: "2fd5d495-c84f-41c1-ac8b-2f5fe7625aac",
  },
  {
    columnId: "otherBasics",
    columnValue: "220000",
    cellId: "649e12c4-bf0a-4200-b43b-bdd7b1737001",
  },
  {
    columnId: "codeInstructions",
    columnValue: "W",
    cellId: "4358d546-b467-424f-b75a-78505070e0c7",
  },
  {
    columnId: "amountOfAdjustment",
    columnValue: "500.00",
    cellId: "c0f540c4-76c2-4dfa-a3b3-28eba7bd7723",
  },
  {
    columnId: "gainOrLoss",
    columnValue: "0.00",
    cellId: "3a7e97e5-a2db-4471-9ae9-b99c992c8aa7",
  },
],
},
{
  rowId: "18247aea-f862-4155-8a67-61c85cfa9f37",
  columns:[
  {
    columnId: "description",
    columnValue: "L 10.00 Corp Action G/L ADN Corp(AQN)",
    cellId: "18dbba72-b130-4641-a007-f1d9f1ea2e47",
  },
  {
    columnId: "dateAcuired",
    columnValue: "2021-09-13 12:55:34",
    cellId: "0ed09f6e-7353-4e32-8979-0c3002dc2a4d",
  },
  {
    columnId: "dateSold",
    columnValue: "2022-03-23 02:45:39",
    cellId: "a491a3c7-78f6-426d-a24c-6f3c98ed345f",
  },
  {
    columnId: "proceeds",
    columnValue: "490.98",
    cellId: "85987acc-cbd0-4f74-914a-b73978792063",
  },
  {
    columnId: "otherBasics",
    columnValue: "100.00",
    cellId: "3db7892f-da9e-46e7-985d-31802f7d958e",
  },
  {
    columnId: "codeInstructions",
    columnValue: "",
    cellId: "2621aed2-3b34-43bd-a642-583e7031b089",
  },
  {
    columnId: "amountOfAdjustment",
    columnValue: "",
    cellId: "2c609a25-7f27-4275-b50e-6f7599433408",
  },
  {
    columnId: "gainOrLoss",
    columnValue: "390.48",
    cellId: "b941b628-59ec-4107-abcb-c8e154a639c4",
  },
],
}
]}

export default {taxFormconfig,shortTermTableData,longTermTableData,checkboxData}
