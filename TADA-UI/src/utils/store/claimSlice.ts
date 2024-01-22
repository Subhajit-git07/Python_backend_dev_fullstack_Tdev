import { AccountInfo, EventType } from "@azure/msal-browser";
import userIcon from '../../assets/img/profile.png'
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

const initialState: reduxStateProps = {
    initializing: false,
    initialized: false,
    idToken: "",
    accessToken: "",
    state: EventType.LOGIN_FAILURE,
     account: [],
    profilePic: userIcon

};
export interface reduxStateProps {
    initializing: boolean,
    initialized: boolean,
    idToken?: string,
    accessToken?: string,
    state: EventType,
    account: any[],
    profilePic: string

}




export const claimSlice = createSlice({
    name: 'claim',
    initialState,
    reducers: {
        updateUserDetails: (state, action: PayloadAction<any>) => {

            switch (action.payload.type) {
                case EventType.INITIALIZE_START:
                    return {
                        ...state,
                        initializing: true,
                        initialized: false,
                    };
                case EventType.INITIALIZE_END:
                    return {
                        ...state,
                        initializing: false,
                        initialized: true,
                    };
                case EventType.ACQUIRE_TOKEN_SUCCESS:
                    return {
                        ...state,
                        account: JSON.parse(action.payload.payload).account,
                        accessToken: JSON.parse(action.payload.payload).accessToken,
                    };
                case EventType.ACQUIRE_TOKEN_FAILURE:
                    return {
                        ...state,

                        accessToken: null,
                    };
                case EventType.LOGIN_SUCCESS:
                    return {
                        ...state,
                        account: action.payload,
                    };
                case EventType.LOGIN_FAILURE:
                case EventType.LOGOUT_SUCCESS:
                    return { ...state, idToken: "", accessToken: "", account: null, state: EventType.LOGIN_FAILURE };
                case "profilePic":
                    return {
                        ...state,
                        profilePic: action.payload
                    }
                default:
                    return state;
            }
        },

    },
})

export const { updateUserDetails } = claimSlice.actions;

export default claimSlice.reducer;