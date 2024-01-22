import React from 'react';
import ReactDOM from 'react-dom/client';
import "antd/dist/antd.css";
import './assets/vendors/base/vendor.bundle.base.css'
import './assets/css/style.css'
import './assets/css/googleapis.css'
import './assets/css/ey-design-system.css'
import './assets/css/login.css'

import './assets/css/tadaStyle.css';
import App from './app';
import { Provider } from "react-redux";
import store  from "./utils/store/store";
const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
   <Provider store={store}>
            <App  />
        </Provider>
  </React.StrictMode>
);


