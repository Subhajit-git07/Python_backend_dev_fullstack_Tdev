
import {  createSlice, PayloadAction } from '@reduxjs/toolkit'
import profileDataType from '../../pages/profile/profileInterface';

const initialState: profileDataType = {
    name: "",
    clientId: String(sessionStorage.getItem('currentClient')?sessionStorage.getItem('currentClient'):""),
    addrLn1:"",
    addrLn2: "",
    city: "",
    state: "",
    zipCode:"",
    country:""

};

export const profileSlice = createSlice({
    name: 'profile',
    initialState,
    reducers: {
        setCurrentProfile:(state,action:PayloadAction<profileDataType>)=>{
            return{...action.payload}
        },
        resetProfile:(state)=>{
            return {...initialState,clientId:""}
        }
    },
})

export const {setCurrentProfile,resetProfile} =profileSlice.actions;

export default profileSlice.reducer;