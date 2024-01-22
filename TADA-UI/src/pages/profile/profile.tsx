import React, { useState } from 'react'
import {
    Button,
    Popconfirm, Select
} from 'antd'
import profileDomain from './profileDomain';
import { isEmpty } from '../../utils/helper';
import profileConstants from '../../utils/constants/profileConstants';
import { LoadingOutlined } from '@ant-design/icons';
import { Spin } from 'antd';
import LoadingOverlay from 'react-loading-overlay-ts';
const { Option } = Select;
const antIcon = (
    <LoadingOutlined
        style={{
            fontSize: 30,
        }}
        spin
    />
);
const Profile = () => {

    const { countries, states,countryChanged, profileData, setProfileData, addNewProfile, updateProfile, deleteProfile, isValid,zipValid, loader, loaderMessage
    } = profileDomain();

    return (

        <LoadingOverlay
            active={loader}
            spinner={<Spin tip={loaderMessage}
                indicator={antIcon}
                style={{ color: "#FFE600" }}
            />}
        >
            <div className="container content-wrapper">
                <div className="col-md-12 p-0">


                    <div className="d-flex mb-3  align-items-center">
                        <div className="col-12 pl-0 mt-3">
                            <h4 className="font-weight-bold mb-0">User Account</h4>
                        </div>

                    </div>

                </div>




                <div className="card mt-3">
                    <div className="card-body">
                        <div className="col-12 row">
                            <div className="col-4 mt-4">
                                <div className="textinput-group">
                                    <input onChange={(e) => {
                                        setProfileData({ ...profileData, name: e.target.value })
                                    }}
                                    data-testid="name" 
                                        value={profileData.name ? profileData.name : ""}
                                        className={`textinput-group__textinput ${(!isValid && isEmpty(profileData.name)) ? "input-required" : ""}`} />
                                    <label className={`textinput-group__label ${isEmpty(profileData.name) ? '' : 'focus'}`} htmlFor="text-input-default2">Name<span className="red">*</span></label>

                                </div>
                            </div>
                            <div className="col-4 mt-4">
                                <div className="textinput-group">
                                    <input className={`textinput-group__textinput ${(!isValid && isEmpty(profileData.taxId)) ? "input-required" : ""}`} onChange={(e) => {
                                        setProfileData({ ...profileData, taxId: e.target.value })
                                    }} data-testid="taxId" 
                                        value={profileData.taxId ? profileData.taxId : ""} />
                                    <label className={`textinput-group__label ${isEmpty(profileData.taxId) ? '' : 'focus'}`} htmlFor="text-input-default5">SSN or Id
                                        <span className="red">*</span></label>
                                </div>
                            </div>
                            <div className="col-4 mt-4">
                                <div className="textinput-group">
                                    <input className={`textinput-group__textinput  ${(!isValid && isEmpty(profileData.formName)) ? "input-required" : ""}`} data-testid="taxId" onChange={(e) => {
                                        setProfileData({ ...profileData, formName: e.target.value })
                                    }} 
                                        value={profileData.formName ? profileData.formName : ""} />
                                    <label className={`textinput-group__label ${isEmpty(profileData.formName) ? '' : 'focus'}`} htmlFor="text-input-default5">Name Shows on return
                                    <span className="red">*</span> </label>
                                </div>
                            </div>
                            <div className="col-4 mt-4">
                                <div className="textinput-group">
                                    <input className={`textinput-group__textinput ${(!isValid && isEmpty(profileData.addrLn1)) ? "input-required" : ""}`} onChange={(e) => {
                                        setProfileData({ ...profileData, addrLn1: e.target.value })
                                    }} data-testid="addrLn1" 
                                        value={profileData.addrLn1 ? profileData.addrLn1 : ""} />
                                    <label className={`textinput-group__label ${isEmpty(profileData.addrLn1) ? '' : 'focus'}`} htmlFor="text-input-default5">Address Line
                                        1<span className="red">*</span></label>
                                </div>
                            </div>

                            <div className="col-4 mt-4">
                                <div className="textinput-group">
                                    <input className={`textinput-group__textinput`} onChange={(e) => {
                                        setProfileData({ ...profileData, addrLn2: e.target.value })
                                    }} data-testid="addrLn2" 
                                        value={profileData.addrLn2 ? profileData.addrLn2 : ""} />
                                    <label className={`textinput-group__label ${isEmpty(profileData.addrLn2) ? '' : 'focus'}`} htmlFor="text-input-default6">Address Line
                                        2</label>
                                </div>
                            </div>
                            <div className="col-4 mt-4">
                                <div className="textinput-group">
                                    <input className={`textinput-group__textinput`} onChange={(e) => {
                                        setProfileData({ ...profileData, city: e.target.value })
                                    }} data-testid="city" 
                                        value={profileData.city ? profileData.city : ""} />
                                    <label className={`textinput-group__label ${isEmpty(profileData.city) ? '' : 'focus'}`} htmlFor="text-input-default7">City</label>
                                </div>
                            </div>
                            <div className="col-4 mt-4">

                                <div className=" dropdown dropdown--single-select">
                                    <Select
                                    data-testid="country" 
                                        showSearch
                                        placeholder=""
                                        onChange={countryChanged}
                                        allowClear
                                        value={profileData.country}
                                        className={`dropdown-toggle ${(!isValid && isEmpty(profileData.country)) ? "input-required" : ""}`}
                                    >
                                        {countries && countries!.map((element, index) =>
                                            <Option key={index} className="dropdown-item" value={element}> {element}</Option>)}


                                    </Select>
                                    <label className={`textinput-group__label ${isEmpty(profileData.country) ? '' : 'focus'}`} htmlFor="text-input-default7">Country<span className="red">*</span></label>



                                </div>
                            </div>
                            <div className="col-4 mt-4">
                                <div className=" dropdown dropdown--single-select">

                                    <Select
                                    data-testid="state" 
                                        showSearch
                                        placeholder=""
                                        onChange={(value) => {
                                            setProfileData({ ...profileData, state: value })
                                        }}
                                        allowClear
                                        value={profileData.state}
                                        className={`dropdown-toggle ${(!isValid && isEmpty(profileData.state)) ? "input-required" : ""}`}
                                    >
                                        {states && states!.map((element, index) =>
                                            <Option key={index} className="dropdown-item" value={element}> {element}</Option>)}


                                    </Select>
                                    <label className={`textinput-group__label ${isEmpty(profileData.state) ? '' : 'focus'}`} htmlFor="text-input-default7">State<span className="red">*</span></label>

                                </div>


                            </div>

                            <div className="col-4 mt-4">

                                <div className="textinput-group">
                                    <input className={`textinput-group__textinput ${((!isValid && isEmpty(profileData.zipCode))||!zipValid) ? "input-required" : ""}`} onChange={(e) => {
                                        setProfileData({ ...profileData, zipCode: e.target.value })
                                    }} data-testid="zipCode" 
                                        value={profileData.zipCode ? profileData.zipCode : ""} />
                                    <label className={`textinput-group__label ${isEmpty(profileData.zipCode) ? '' : 'focus'}`}
                                        htmlFor="text-input-default8">Zipcode<span className="red">*</span></label>
                                </div>
                           
                            </div>

                            <div className="col-12 row mt-4">
                                {profileData.clientId ?
                                    <>
                                        <div className="col-2">
                                            <Popconfirm
                                                title="Are you sure you want to update this details?"
                                                onConfirm={updateProfile}
                                                okText="Yes"
                                                cancelText="No"
                                            >   <Button className=' text-center btn btn--progress btn--primary' >Update</Button></Popconfirm>
                                        </div>
                                        <div className="col-2">
                                            <Popconfirm

                                                title="Are You sure You want to delete this client?"
                                                onConfirm={deleteProfile}
                                                okText="Delete"
                                                cancelText="Cancel"
                                            > <Button className=' text-center btn btn--progress btn--primary' type="primary" danger>Delete</Button>
                                            </Popconfirm>
                                        </div>
                                    </>
                                    : <div className="col-2">
                                        <button onClick={() => addNewProfile()} className=" text-center btn btn--progress btn--primary" title="Button">
                                            Create</button>
                                    </div>}
                                <div className="col-md-4 ">
                                    {!isValid && <span className="red fonts-col__sub-title mt-2">*Please Enter Required Fields</span>}
                                    {(isValid && !zipValid) &&    <span className="red fonts-col__sub-title mt-2">Enter Proper ZipCode</span>}
                                </div>
                            </div>
                        </div>
                    </div>
                </div></div>
        </LoadingOverlay>
    );
}
export default Profile
