import profileDataType from "./profileInterface";
import React, { useEffect, useState } from "react";
import { message, TableProps } from "antd";
import { useMsal } from "@azure/msal-react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { profileStore } from "../../utils/store/store";
import profileService from "../../services/api/profileService";
import profileConstants from '../../utils/constants/profileConstants';
import { isValidPostalCode, objectValidationByEachProp, openNotification } from "../../utils/helper";
import { resetProfile, setCurrentProfile } from "../../utils/store/profileSlice";
import Logger from '../../services/azure/appInsights/Logger/logger';
import { SeverityLevel } from "@microsoft/applicationinsights-web";
import { v4 as uuidv4 } from 'uuid';
import messages from '../../utils/constants/messages';

const profileDomain = () => {
  const currentProfile = useSelector(profileStore)
  const dispatch = useDispatch();
  const { instance, accounts } = useMsal();
  const [isValid, setIsValid] = useState<boolean>(true);
  const [zipValid, setZipValid] = useState<boolean>(true);
  const [profileData, setProfileData] = useState<profileDataType>(currentProfile)
  const [loader, setLoader] = useState(false);
  const [loaderMessage, setloaderMessage] = useState("");
  const [states, setStates] = useState<string[]>();
  const [countries, setCountries] = useState<string[]>();
  const navigate = useNavigate();
  useEffect(() => {
    if (currentProfile.clientId) {
      getCurrentProfile();
    }
    else {
      setProfileData({
        name: "",
        clientId: "",
        addrLn1: "",
        addrLn2: "",
        city: "",
        state: "",
        zipCode: "",
        country: "", ...currentProfile
      });
    } getCountries();
  }, [currentProfile])

  const getCountries = () => {
    Logger.trackTrace({ message: "Get countries for profile page",  severityLevel: SeverityLevel.Information })
    profileService.getCountries(instance, accounts).then((response: string[]) => {
    setCountries(response)
      Logger.trackTrace({ message: "returned countries", data: `response =${JSON.stringify(response)}`, severityLevel: SeverityLevel.Information })
    }).catch((err) => {
      message.warning("Error while getting the countries  for Profile page")
      Logger.trackException({ message: err })
    })
  }
  const countryChanged = (country: string) => {
    Logger.trackTrace({ message: "Get states for the selected country",data:`country=${country}` , severityLevel: SeverityLevel.Information })
    profileService.getStates(instance, accounts,country).then((response: string[]) => {
      setStates(response)
      Logger.trackTrace({ message: "returned states", data: `response =${JSON.stringify(response)}`, severityLevel: SeverityLevel.Information })
    }).catch((err) => {
      message.warning(`Error while getting the states  for country= ${country}`)
      Logger.trackException({ message: err })
    })
    setStates(profileConstants.States.filter(function (eachState) { return eachState.country == country }).map(function (eachresult) { return eachresult.state }))
    setProfileData({ ...profileData, country: country, state: "" })
  }
  const getCurrentProfile = () => {
    setLoader(true);
    setloaderMessage("Geting User Profile details Please wait ...");
    Logger.trackTrace({ message: "Get selected Profile details", data: `id =${String(currentProfile.clientId)}`, severityLevel: SeverityLevel.Information })
    profileService.getProfile(instance, accounts, currentProfile.clientId!).then((response: profileDataType) => {
      setProfileData(response)
      setLoader(false);
      setloaderMessage("");
      Logger.trackTrace({ message: "returned selected profile Values", data: `response =${JSON.stringify(response)}`, severityLevel: SeverityLevel.Information })
    }).catch((err) => {
      message.warning("Error while getting the selected user Profile")
      Logger.trackException({ message: err })
      dispatch(resetProfile());
      setLoader(false);
      setloaderMessage("");
    })
  }
  const addNewProfile = () => {
    if (objectValidationByEachProp(profileData, ["name","formName", "addrLn1", "state", "zipCode", "country","taxId"])) {
      setIsValid(true);
      if (isValidPostalCode(profileData.zipCode!, profileData.country!)) {
        setZipValid(true);

        setLoader(true);
        setloaderMessage("Adding New profile plase wait...");
        Logger.trackEvent({ name: "Create Profile", data: `data =${JSON.stringify(currentProfile)}` })
        Logger.trackTrace({ message: "create Profile ", data: `data =${JSON.stringify(currentProfile)}`, severityLevel: SeverityLevel.Information })
        profileData.clientId = uuidv4();
        profileService.addNewProfile(instance, accounts, profileData, accounts[0].username!).then(function (response) {
          if (response == messages.addClient) {
            setLoader(false);
            setloaderMessage("");
            dispatch(setCurrentProfile(currentProfile))
            message.success(messages.addClient)
            Logger.trackTrace({ message: messages.addClient, data: `response =${JSON.stringify(response)}`, severityLevel: SeverityLevel.Information })
            navigate("/TADA/profileSummary")
          }
        }).catch((err) => {
          setProfileData({ ...profileData, clientId: "" })
          Logger.trackTrace({ message: messages.addClientError, data: `err =${JSON.stringify(err)}`, severityLevel: SeverityLevel.Error })
          Logger.trackException({ message: err })
          message.error(messages.addClientError)
          setLoader(false);
          setloaderMessage("");
        })
      }
      else {
        setZipValid(false);
      }
    }
    else {
      setIsValid(false);
    }
  }
  const updateProfile = () => {
    if (objectValidationByEachProp(profileData, ["name","formName", "addrLn1", "state", "zipCode", "country","taxId"])) {
      setIsValid(true);
      if (isValidPostalCode(profileData.zipCode!, profileData.country!)) {
        setZipValid(true);
        setLoader(true);
        setloaderMessage("Updating profile details Please wait ...");
        Logger.trackEvent({ message: "udpate Profile details", data: `data =${JSON.stringify(currentProfile)}` })
        Logger.trackTrace({ message: "udpate Profile details", data: `data =${JSON.stringify(currentProfile)}`, severityLevel: SeverityLevel.Information })
        profileService.updateProfile(instance, accounts, profileData).then(function (response) {
          if (response == messages.updateClient) {
            setLoader(false);
            setloaderMessage("");
            message.success(messages.updateClient)
            Logger.trackTrace({ message: messages.updateClient, data: `response =${JSON.stringify(response)}`, severityLevel: SeverityLevel.Information })
            navigate("/TADA/profileSummary")
          }
        }).catch((err) => {
          Logger.trackException({ message: err })
          message.error(messages.updateClientError)
          setLoader(false);
          setloaderMessage("");
        })
      } else {
        setZipValid(false);
      }
    } else {
      setIsValid(false);
    }
  }
  const deleteProfile = () => {
    setLoader(true);
    setloaderMessage("Deleting User Please wait ...");
    Logger.trackEvent({ message: "Delete Client details", data: `id =${JSON.stringify(currentProfile.clientId)}`, severityLevel: SeverityLevel.Information })
    profileService.deleteProfile(instance, accounts, currentProfile.clientId!).then(function (response) {

      if (response == messages.deleteClient) {
        dispatch(resetProfile());
        setLoader(false);
        setloaderMessage("");
        message.success(messages.deleteClient)
        Logger.trackTrace({ message: messages.deleteClient, data: `id=${currentProfile.clientId!},response =${JSON.stringify(response)}`, severityLevel: SeverityLevel.Information })
        navigate("/TADA/profileSummary")
      }
    }).catch((err) => {
      setLoader(false);
      setloaderMessage("");
      Logger.trackTrace({ message: messages.deleteClientError, data: `err =${JSON.stringify(err)}`, severityLevel: SeverityLevel.Error })
      Logger.trackException({ message: err, severityLevel: SeverityLevel.Error })
      message.error(messages.deleteClientError)
    })
  }

  return { countries, states, countryChanged, profileData, setProfileData, addNewProfile, updateProfile, deleteProfile, isValid, zipValid, loader, loaderMessage }
}
export default profileDomain 