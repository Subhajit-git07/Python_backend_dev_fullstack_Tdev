import {Checkbox, Divider, Image, Popconfirm, Typography } from 'antd';
import type { CheckboxChangeEvent } from 'antd/es/checkbox';
import React from 'react';
import PS from '../../assets/img/PS.png';
import transaction from '../../assets/img/transaction.png';
import classification from '../../assets/img/classification.png';
import taxSummary from '../../assets/img/taxSummary.png';
import userAccount from '../../assets/img/userAcount.png';
import documents from '../../assets/img/documents.png';
import analytics from '../../assets/img/analytics.png';

const { Title, Paragraph, Text, Link } = Typography;

const navigation = () => {
    const confirm = () => {
        console.log('Clicked on Yes.');
      };
    return(  
        <div className="container content-wrapper">
          <div className="mb-2 row">
          <div className="card col-12 mt-3">
              <div className="card-body">
              <div className="row mt-5">
                <div className="col-6">
                <div className='numberList'>
                1</div>
                <div className='informationText'>
                <Typography>
                    <Title level={3}>Profile Summary</Title>
                    <Paragraph>
                    Profile Summary page contains the information about Net Portfolio Values,Estimated Tax liability and Holdings.
                     It Gives the detail information about clients In and Out Portfolio Values,Short term capital gain(STCG),Long term capital gain(LTCG) liability details and clients In and Out holding Values.Following are the key points:
                    </Paragraph>
                    <Paragraph>
                        <ul className='dataList'>
                            <li>
                            Net Portfolio Value
                            </li>
                            <li>
                            Estimated tax liability
                            </li>
                            <li>
                           Holdings
                            </li>
                        </ul>
                        </Paragraph>
                        <Paragraph>
                        <a href="/TADA/profileSummary">
                            {' '}
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                           Get Started
                            </button>
                         </a>
                        </Paragraph>
                </Typography>
                </div>
                </div>
                <div className="col-6 imgStyle">
                    <div>
                    <Image
                        width={350}
                        height={350}
                        src={PS}
                    />
                </div>
                </div>
               </div>
               
               <div className="row mt-5">
               <div className="col-6 imgStyle">
                    <div>
                    <Image
                        width={350}
                        height={350}
                        src={transaction}
                    />
                </div>
                </div>
                <div className="col-6">
                <div className='numberList'>
                2</div>
                <div className='informationText'>
                <Typography>
                    <Title level={3}>Transactions</Title>
                    <Paragraph>
                    Transaction page gives the information of all the transactions.We can add transactions from add wallet address, add exchange and add manually.
                    We can download the all the transactions from this page.Following are the links to add the transactions:
                    </Paragraph>
                    <Paragraph>
                        <ul className='dataList'>
                            <li>
                            <Link href="/TADA/addtransactions/wallet" style={{color:'inherit'}}><i className="material-icons listLink">link</i>Add Wallet Address</Link>
                            </li>
                            <li>
                            <Link href="/TADA/addtransactions/exchange" style={{color:'inherit'}}><i className="material-icons listLink">link</i>Add Exchange</Link>
                            </li>
                            <li>
                            <Link href="/TADA/addtransactions/manual" style={{color:'inherit'}}><i className="material-icons listLink">link</i>Add Manually</Link>
                            </li>
                        </ul>
                        </Paragraph>
                        <Paragraph>
                        <a href="/TADA/transactions">
                            {' '}
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                           Get Started
                            </button>
                         </a>
                        </Paragraph>
                </Typography>
                </div>
                </div>
               </div>
               <div className="row mt-5">
                <div className="col-6">
                <div className='numberList'>
                3</div>
                <div className='informationText'>
                <Typography>
                    <Title level={3}>Classification</Title>
                    <Paragraph>
                    Classification page contains the information about unclassified transactions.Using this page we can update the transactions data manually and then can classify the transactios.followings are the key points:
                    </Paragraph>
                    <Paragraph>
                        <ul className='dataList'>
                            <li>
                             Classify data
                            </li>
                            <li>
                            Update unclassified data
                            </li>
                        </ul>
                        </Paragraph>
                        <Paragraph>
                        <a href="/TADA/classification">
                            {' '}
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                           Get Started
                            </button>
                         </a>
                        </Paragraph>
                </Typography>
                </div>
                </div>
                <div className="col-6 imgStyle">
                    <div>
                    <Image
                       width={350}
                        height={350}
                        src={classification}
                    />
                </div>
                </div>
               </div>
               <div className="row mt-5">
               <div className="col-6 imgStyle">
                    <div>
                    <Image
                       width={350}
                        height={350}
                        src={taxSummary}
                    />
                </div>
                </div>
                <div className="col-6">
                <div className='numberList'>
                4</div>
                <div className='informationText'>
                <Typography>
                    <Title level={3}>Tax Summary</Title>
                    <Paragraph>
                    Tax Summary page gives the information about fifo,lifo and hifo data.From this page we can directly download the BCA-Tax Template.
                    By selecting tax form type and year we can redirect to the perticular tax form.followings are the key points: 
                    </Paragraph>
                    <Paragraph>
                        <ul className='dataList'>
                            <li>
                            BCA-Tax Template
                            </li>
                            <li>
                           Tax Form
                            </li>
                            <li>
                           fifo,lifo,hifo details
                            </li>
                        </ul>
                        </Paragraph>
                        <Paragraph>
                        <a href="/TADA/viewtaxliability">
                            {' '}
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                           Get Started
                            </button>
                         </a>
                        </Paragraph>
                </Typography>
                </div>
                </div>
               </div>
               <div className="row mt-5">
                <div className="col-6">
                <div className='numberList'>
                5</div>
                <div className='informationText'>
                <Typography>
                    <Title level={3}>User Accounts</Title>
                    <Paragraph>
                   Use Accounts page gives the detail information about the selected Client.We can add new client,Update client details and delete perticular client using this page.
                   Followings are the key points:
                    </Paragraph>
                    <Paragraph>
                        <ul className='dataList'>
                            <li>
                           Add Client
                            </li>
                            <li>
                            Update Client
                            </li>
                            <li>
                            Delete Client
                            </li>
                        </ul>
                        </Paragraph>
                        <Paragraph>
                        <a href="/TADA/profile">
                            {' '}
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                           Get Started
                            </button>
                         </a>
                        </Paragraph>
                </Typography>
                </div>
                </div>
                <div className="col-6 imgStyle">
                    <div>
                    <Image
                       width={350}
                        height={350}
                        src={userAccount}
                    />
                </div>
                </div>
               </div>
               <div className="row mt-5">
               <div className="col-6 imgStyle">
                    <div>
                    <Image
                       width={350}
                        height={350}
                        src={documents}
                    />
                </div>
                </div>
                <div className="col-6">
                <div className='numberList'>
                6</div>
                <div className='informationText'>
                <Typography>
                    <Title level={3}>Documents</Title>
                    <Paragraph>
                    Documents page can be used to download different type of tax forms.By selecting year and tax form type user can able to download
                    perticular tax form.Followings are the key points:
                    </Paragraph>
                    <Paragraph>
                        <ul className='dataList'>
                            <li>
                            Download Tax form
                            </li>
                           
                        </ul>
                        </Paragraph>
                        <Paragraph>
                        <a href="/TADA/taxFormDocuments">
                            {' '}
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                           Get Started
                            </button>
                         </a>
                        </Paragraph>
                </Typography>
                </div>
                </div>
               </div>
               <div className="row mt-5">
                <div className="col-6">
                <div className='numberList'>
                7</div>
                <div className='informationText'>
                <Typography>
                    <Title level={3}>Analytics</Title>
                    <Paragraph>
                    Analytics page contains the different types of analytical charts like line charts,pie charts etc.
                    This page gives us a facility to add this charts/components to the profile summary page.followings are the key points:
                    </Paragraph>
                    <Paragraph>
                        <ul className='dataList'>
                            <li>
                            Pin/Unpin functionality for profile summary page
                            </li>
                            <li>
                           Types of  charts
                            </li>
                        </ul>
                        </Paragraph>
                        <Paragraph>
                        <a href="/TADA/analytics">
                            {' '}
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                           Get Started
                            </button>
                         </a>
                        </Paragraph>
                </Typography>
                </div>
                </div>
                <div className="col-6 imgStyle">
                    <div>
                    <Image
                       width={350}
                        height={350}
                        src={analytics}
                    />
                </div>
                </div>
               </div>
              </div>
              <Divider />
              
              <div className='m-3'>
              <Title level={5} className='stopPageMsg'>Do you want to stop seeing this page after each log in?</Title>
              <Popconfirm placement="top" title={"You will be redirect to profile summary page after log in.You can visit this page from left side navigation.Are you sure to stop seeing this page?"} onConfirm={confirm} okText="Yes" cancelText="No">
                            <button
                            className="btn btn--progress btn--primary"
                            title="Button"
                            >
                          Submit
                            </button>
                            </Popconfirm>
              </div>
              
             
  </div>
  </div>
  
  </div>
    )
};

export default navigation;