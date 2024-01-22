
import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom';


const AddTransactionDomain = () => {
    const [currentRoute, setCurrentRoute] = useState<string>("wallet");
    const { pathname } = useLocation();
    useEffect(() => {
        
        setCurrentRoute(pathname.split('/').pop()!)
    }, [pathname])
    return {
        currentRoute,
        setCurrentRoute

    }
}
export default AddTransactionDomain
