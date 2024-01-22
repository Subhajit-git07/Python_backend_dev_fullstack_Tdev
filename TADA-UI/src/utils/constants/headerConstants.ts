import moment from "moment"

const notifications = [
    {
        name: "John Jr",
        description: "Calssification Completed for the Client John",
        date: moment().format("LLL")
    },
    {
        name: "Peter Gibb",
        description: "8949 Document generated for Peter",
        date: "Sep 25, 2022"
    },
    {
        name: "Max Joe",
        description: "Please add missing classification details for the client Max",
        date: "Aug 17, 2022"
    },
    {
        name: "Test Client",
        description: "New Client Maari Created Successfully",
        date: "Aug 01, 2022"
    },
]
const tasks = [
    {
        name: "8949 generation pending",
        description: "For client Peter",
        date: moment().add(7).format("LLL"),
        status: "Not Started"
    },
    {
        name: "Return submission pending",
        description: "Finiancial year 2021-22",
        date: "Jul 31, 2022",
        status: "Not Started"
    },
    {
        name: "Tax submission Pending",
        description: "Finiancial year 2022-23",
        date: "Apr 31, 2023",
        status: "Not Started"
    },
]

const news = [
    {
        img: require("../../assets/images/news/news1.jpg"),
        heading: "EY Value Realized 2022 – have you read our global annual report?",
        description: "Have you read EY Value Realized 2022? The global annual report summarizes the many positive impacts we have on our colleagues, clients and society.",
        navLink: "https://intranet.ey.com/newsviews/829204/ey-value-realized-2022-have-you-read-our-global-annual-report"

    },
    {
        img: require("../../assets/images/news/news2.jpg"),
        heading: "Webcast replay: Sustainability and Technology | Hype, Innovation, and Impact",
        description: "Did you miss the latest Tech Talk on Sustainability and Technology? If you were unable to attend or would like to revisit some of the key points shared by Dr. Krishnaswamy Sankaran, Global Sustainability Technology Officer, during the session, you can watch a replay here. Slides presented during the talk can be found here. ",
        navLink: "https://intranet.ey.com/sites/technology-content/newsviews/831155/tech-talks"

    },
    {
        img: require("../../assets/images/news/news3.jpg"),
        heading: "Catch up with the EMEIA Sustainability webcast series, ahead of COP27",
        description: "In FY22, we hosted the first four episodes of the EMEIA Sustainability webcast series, each of which had a distinct theme and addressed three pertinent questions. They were all well attended by both EY people and clients alike",
        navLink: "https://intranet.ey.com/newsviews/829218/catch-up-with-the-emeia-sustainability-webcast-series-ahead-of-cop27"

    },
]
export default { notifications, tasks,news }