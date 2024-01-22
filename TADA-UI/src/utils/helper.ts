import { notification } from "antd";
import { useEffect, useRef } from "react";

interface NotificationDataType {
    message: string,
    description: string,
}

const openNotification = (notificationData: NotificationDataType) => {
    notification.open({
        message: notificationData.message,
        description: notificationData.description,
        duration: 2
    });
};

const isEmpty = (value: any) => {
    if (value == "" || value == undefined || value == null  ) {
        return true;
    }
    else {
        return false
    }
}
const ExcelDateToJSDate=(serial:number) =>{
    var utc_days  = Math.floor(serial - 25569);
    var utc_value = utc_days * 86400;                                        
    var date_info = new Date(utc_value * 1000);
 
    var fractional_day = serial - Math.floor(serial) + 0.0000001;
 
    var total_seconds = Math.floor(86400 * fractional_day);
 
    var seconds = total_seconds % 60;
 
    total_seconds -= seconds;
 
    var hours = Math.floor(total_seconds / (60 * 60));
    var minutes = Math.floor(total_seconds / 60) % 60;
 
    return new Date(date_info.getFullYear(), date_info.getMonth(), date_info.getDate(), hours, minutes, seconds);
 }
const numberIntoCurrency = (labelValue: number) => {

    // Nine Zeroes for Billions
    return `$${Math.abs(Number(labelValue)) >= 1.0e+30

        ? (Math.abs(Number(labelValue)) / 1.0e+30).toFixed(2) + "n":
        
        Math.abs(Number(labelValue)) >= 1.0e+27

        ? (Math.abs(Number(labelValue)) / 1.0e+27).toFixed(2) + "o":
        
        Math.abs(Number(labelValue)) >= 1.0e+24

        ? (Math.abs(Number(labelValue)) / 1.0e+24).toFixed(2) + "S":
        Math.abs(Number(labelValue)) >= 1.0e+21

        ? (Math.abs(Number(labelValue)) / 1.0e+21).toFixed(2) + "s":
        Math.abs(Number(labelValue)) >= 1.0e+18

        ? (Math.abs(Number(labelValue)) / 1.0e+18).toFixed(2) + "Q":
        Math.abs(Number(labelValue)) >= 1.0e+15

        ? (Math.abs(Number(labelValue)) / 1.0e+15).toFixed(2) + "q":
        Math.abs(Number(labelValue)) >= 1.0e+12

        ? (Math.abs(Number(labelValue)) / 1.0e+12).toFixed(2) + "t":
        Math.abs(Number(labelValue)) >= 1.0e+9

        ? (Math.abs(Number(labelValue)) / 1.0e+9).toFixed(2) + "B"
        // Six Zeroes for Millions 
        : Math.abs(Number(labelValue)) >= 1.0e+6

            ? (Math.abs(Number(labelValue)) / 1.0e+6).toFixed(2) + "M"
            // Three Zeroes for Thousands
            : Math.abs(Number(labelValue)) >= 1.0e+3

                ? (Math.abs(Number(labelValue)) / 1.0e+3).toFixed(2) + "K"

                : Math.abs(Number(labelValue)).toFixed(2)}`;

}
const objectValidation = (object: any) => {
    let formValid = true;
    Object.keys(object).map((fieldName, i) => {
        if (formValid && isEmpty(object[fieldName])) {
            formValid = false;
        }
    });
    return formValid;
}
const objectValidationByEachProp = (object: any, dataFields: string[]) => {
    let formValid = true;
    dataFields.map((eachprop) => {
        if (formValid && isEmpty(object[eachprop])) {
            formValid = false;
        }
    })
    return formValid;
}
function getRndIntegerBetWeen(min: number, max: number) {
    return Math.floor(Math.random() * (max - min)) + min;
}

const useInterval = (callback: () => void, delay: number | null) => {
    const savedCallback = useRef<() => void>();

    // Remember the latest callback.
    useEffect(() => {
        // ①
        savedCallback.current = callback;
    }, [callback]);

    // Set up the interval.
    useEffect(() => {
        function tick() {
            // ②
            savedCallback.current && savedCallback.current();
        }
        if (delay !== null) {
            const id = setInterval(tick, delay);
            return () => clearInterval(id);
        }
    }, [delay]);
};
const  isValidPostalCode=(postalCode:string, countryCode:string)=> {
    let postalCodeRegex:RegExp;
    switch (countryCode) {
        case "United States":
            postalCodeRegex =/^\d{5}(-\d{4})?$/;
            break;
        // case "CA":
        //     postalCodeRegex = /^([A-Z][0-9][A-Z])\s*([0-9][A-Z][0-9])$/;
        //     break;
        default:
            postalCodeRegex = /^(?:[A-Z0-9]+([- ]?[A-Z0-9]+)*)?$/;
    }
    return postalCodeRegex.test(postalCode);
}

const setImagePath = (imgName: string, type?: string) => {
    try {
        return require(`../assets/img/${imgName}.png`)
    } catch {
        if (type == "nft")
            return require(`../assets/img/nft.png`)
        else {
            return require(`../assets/img/crypto.png`)
        }

    }
}
const paginate=(array:any[],  page_number:number,page_size:number)=> {
    // human-readable page numbers usually start with 1, so we reduce 1 in the first argument
    return array.slice((page_number - 1) * page_size, page_number * page_size);
  }

  function getInitials(nameString: String) {
    const fullName = nameString.split(' ');
    const initials = fullName.shift()!.charAt(0) + fullName.pop()!.charAt(0);
    return initials.toUpperCase();
  }

export { openNotification,paginate, isEmpty, setImagePath, numberIntoCurrency, objectValidation,objectValidationByEachProp, getRndIntegerBetWeen, useInterval ,isValidPostalCode,ExcelDateToJSDate,getInitials}