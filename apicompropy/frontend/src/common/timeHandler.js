const moment = require('moment')

let getTime;
getTime = (time) => {
    moment.locale('ru')
    return moment(String(time)).format("Do MMMM, YYYY")
    }

export {getTime};