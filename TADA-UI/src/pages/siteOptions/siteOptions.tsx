import {Checkbox, Divider, Image, Popconfirm, Typography } from 'antd';

import React from 'react';


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
                   <div className="col-md-12 p-0">
                    <div className="d-flex mb-3  align-items-center">
                        <div className="col-12 pl-0 mt-3">
                            <h3 className="font-weight-bold mb-0" style={{textAlign:'center'}}>Site Options</h3>
                        </div>

                    </div>

                    </div>

                    <div className="row mt-5 boxClass">
                      <div className="m-4">
                      <Link href="/TADA/profileSummary" style={{color:'inherit'}}><button className='rectangle'> <i className="material-icons optionsIcon"> home</i>Profile Summary</button>
                      </Link> </div>
                      <div className="m-4">
                      <Link href="/TADA/transactions" style={{color:'inherit'}}><button className='rectangle'><i className="material-icons optionsIcon">swap_horiz</i>Transactions</button>
                      </Link> </div>
                      <div className="m-4"> 
                      <Link href="/TADA/classification" style={{color:'inherit'}}><button className='rectangle'><i className="material-icons optionsIcon">edit</i>Classification</button>
                      </Link>  </div>
                      <div className="m-4">
                      <Link href="/TADA/viewtaxliability" style={{color:'inherit'}}> <button className='rectangle'> <i className="material-icons optionsIcon"> feed</i>Tax Summary</button>
                      </Link></div>
                      
                    </div>
                    <div className="row mt-5 boxClass">
                      <div className="m-4">
                      <Link href="/TADA/profile" style={{color:'inherit'}}><button className='rectangle'> <i className="material-icons optionsIcon">manage_accounts</i>
                      User Accounts</button></Link>
                      </div>
                      <div className="m-4">
                      <Link href="/TADA/taxFormDocuments" style={{color:'inherit'}}><button className='rectangle'><i className="material-icons optionsIcon">menu_book</i>Documents</button>
                      </Link></div>
                      <div className="m-4">
                      <Link href="/TADA/analytics" style={{color:'inherit'}}><button className='rectangle'> <i className="material-icons optionsIcon">assessment</i>Analytics</button>
                      </Link></div>
                      <div className="m-4">
                      <Link href="/TADA/getStarted" style={{color:'inherit'}}><button className='rectangle'><i className="material-icons optionsIcon">not_started</i>Get Started</button>
                      </Link></div>
                      
                    </div>

              </div>    
             
  </div>
  </div>
  
  </div>
    )
};

export default navigation;