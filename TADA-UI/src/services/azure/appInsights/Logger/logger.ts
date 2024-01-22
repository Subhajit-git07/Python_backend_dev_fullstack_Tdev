import { SeverityLevel } from "@microsoft/applicationinsights-web"
import { appInsights } from "../appInsights"
import loggerDataType from "./loggerInterface"




const trackEvent = (logger: loggerDataType) => {
    appInsights.trackEvent({ name: logger.name!, properties: { data: logger.data } })
}
const trackTrace = (logger: loggerDataType) => {
    appInsights.trackTrace({ message: logger.message!, severityLevel: logger.severityLevel, properties: { data: logger.data } })
}
const trackException = (logger: loggerDataType) => {
    appInsights.trackException({ error: new Error(logger.message), severityLevel: SeverityLevel.Error })

}

export default { trackEvent, trackTrace, trackException }