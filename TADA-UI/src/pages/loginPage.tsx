import * as React from 'react'
import { Link } from "react-router-dom";
import { PlusOutlined } from '@ant-design/icons';
const loginPage:React.FC = () => {

    return (
        <div className="row">
            <div className="login-left">

                <div className="login-right">
                    <div className="login-logo">
                        {/* <img alt="EY Logo" className="global-header__tittle__image" src={Logo} /> */}

                        <span className="global-header__tittle__label">Crypto TADA</span>

                    </div>

                    <div className="login-content">
                        <label> Let's get started</label>
                     
                        <a href="" className="forgtpass d-flex">
                        <PlusOutlined /> add
                        Login another account</a>
                        <Link to="/TADA">  <button className="btn btn--primary spacing-05-m-t btn-eyuser" title="Button"> I am an EY employee</button>
                        </Link>
                        <button className="btn btn--primary spacing-03-m-t btn-noneyuser" title="Button"> I am not an Ey employee</button>

                    </div>
                </div>
            </div>
        </div>


    )
}
export default loginPage