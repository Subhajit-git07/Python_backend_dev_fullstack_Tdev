
import { EventType } from "@azure/msal-browser";
import { configureStore, createSlice, PayloadAction } from '@reduxjs/toolkit'
import userIcon from '../assets/img/ey-logo.svg'
import   claimSlice  from './claimSlice'
import profileSlice from './profileSlice'

const store = configureStore({
    reducer: {
        claims: claimSlice,
        profile:profileSlice,
    },
})
type RootState = ReturnType<typeof store.getState>;
export const claimsStore = (state: RootState) => state.claims
export const profileStore =(state: RootState) => state.profile
export default store;
