// AppInsights.js
import { ApplicationInsights } from '@microsoft/applicationinsights-web'
import { ReactPlugin, withAITracking } from '@microsoft/applicationinsights-react-js'
import { ComponentType } from 'react';
import { authConfig } from '../../../utils/config'


const reactPlugin = new ReactPlugin();
const ai = new ApplicationInsights({
    config: {
        instrumentationKey:authConfig.appInsightKey,
        enableAutoRouteTracking: true,
        extensions: [reactPlugin]
    }
})
ai.loadAppInsights()

export default (Component: ComponentType<unknown>) => withAITracking(reactPlugin, Component)
export const appInsights = ai.appInsights