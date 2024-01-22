import { Dropdown, Menu, message } from 'antd';
import React from 'react'
import { NavigateFunction, useNavigate } from 'react-router-dom';
import { PinMenuProps } from '../analyticsInterface';
const PinMenuOptions = (props: PinMenuProps) => {
    const navigate = useNavigate();
    let myPreferences: PinMenuProps[] = JSON.parse(localStorage.getItem("MyPreferences")!)
    return (
        <Menu
            items={[
                {
                    key: 'pin',
                    label: ((myPreferences && myPreferences.filter((eachSelection) => { return eachSelection.name == props.name }).length > 0) ?
                        (<span onClick={() => { pintoProfile(props, false,navigate) }}>
                            Un Pin into Profile Page
                        </span>
                        ) : (<span onClick={() => { pintoProfile(props, true,navigate) }}>
                            Pin into Profile Page
                        </span>)),
                },

            ]}
        />

    );
}
const PinMenu = (props: PinMenuProps) => {
  
    return (<Dropdown className='pl-1' trigger={['click']} overlay={PinMenuOptions(props)} placement="bottom">
        <a >  <i className="tasks material-icons text-center" > more_horiz </i></a>
    </Dropdown>)
}

const pintoProfile = (selectedDetails: PinMenuProps, isPin: boolean,navigate:NavigateFunction) => {


    if (localStorage.getItem("MyPreferences")) {
        let myPreferences: PinMenuProps[] = [];
        myPreferences = JSON.parse(localStorage.getItem("MyPreferences")!)
        if (!isPin) {
            myPreferences = myPreferences.filter((eachProp) => { return eachProp.name != selectedDetails.name })
            navigate(0)
        }
        else if (myPreferences.length < 2 && isPin) {
            myPreferences.push(selectedDetails)
            navigate(0)
        }
        else {
            message.warning("You can pin only max of 2 items only")
        }
        localStorage.setItem("MyPreferences", JSON.stringify(myPreferences))

    }
    else {
        localStorage.setItem("MyPreferences", JSON.stringify([selectedDetails]))
        navigate(0)
    }



}
export default PinMenu