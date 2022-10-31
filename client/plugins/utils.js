class Utils {
  static COOKIE_KEY = ["skill_mgmt_sys_user_id", "skill_mgmt_sys_company_id", "skill_mgmt_sys_auth"];
  static crypto = require("crypto");

  static saveLoginInfo(token, id, company, auth) {
    this.saveCookie(this.COOKIE_KEY[0], encodeURIComponent(id));
    this.saveCookie(this.COOKIE_KEY[1], encodeURIComponent(company));
    this.saveCookie(this.COOKIE_KEY[2], encodeURIComponent(auth));
  }

  static clearLoginInfo() {
    document.cookie = `${this.COOKIE_KEY[0]}=;max-age=0`;
    document.cookie = `${this.COOKIE_KEY[1]}=;max-age=0`;
    document.cookie = `${this.COOKIE_KEY[2]}=;max-age=0`;
  }

  static saveCookie(key, text) {
    document.cookie = key + '=' + text + '; ' + 'SameSite=lax;';
  }

  static getCookieArray(){
    var arr = new Array();
    if(document.cookie != ''){
      var tmp = document.cookie.split('; ');
      for(var i=0;i<tmp.length;i++){
        var data = tmp[i].split('=');
        if(this.COOKIE_KEY.includes(data[0])) {
          arr[data[0]] = decodeURIComponent(data[1]);
        }
      }
    }
    return arr;
  }

  static getCookieData(key){
    if(document.cookie != ''){
      var tmp = document.cookie.split('; ');
      for(var i=0;i<tmp.length;i++){
        var data = tmp[i].split('=');
        if(data[0] === key) {
          return decodeURIComponent(data[1]);
        }
      }
    }
  }

  static getUserId() {
    return this.getCookieData(this.COOKIE_KEY[0]);
  }

  static getCompanyId() {
    return this.getCookieData(this.COOKIE_KEY[1]);
  }

  static getAuth() {
    return this.getCookieData(this.COOKIE_KEY[2]);
  }

  static GetDate(val) {
    if(val == null) return val;
    
    var valDate = new Date(val);
    var  month = ("0"+(valDate.getMonth() + 1)).slice(-2)
    var date =  ("0"+valDate.getDate()).slice(-2)
    var year = valDate.getFullYear()
    var array = [year, month, date]
    var resultDate = array.join('-')
    return resultDate
  }

  static GetSlashDate(val) {
    if(val == null) return val;

    var valDate = new Date(val);
    var year = valDate.getFullYear()
    var month = ("0"+(valDate.getMonth() + 1)).slice(-2)
    var day =  ("0"+valDate.getDate()).slice(-2)
    var array = [year, month, day]
    var resultDate = array.join('/')
    return resultDate
  }

  static GetSlashDateTime(val) {
    if(val == null) return val;

    var valDate = new Date(val);
    var year = valDate.getFullYear()
    var month = ("0"+(valDate.getMonth() + 1)).slice(-2)
    var day =  ("0"+valDate.getDate()).slice(-2)
    var date = [year, month, day]
    var slashDate = date.join('/')

    var hours = ("0"+(valDate.getHours())).slice(-2)
    var minutes =  ("0"+valDate.getMinutes()).slice(-2)
    var time = [hours, minutes]
    var resultDate = slashDate + ' ' + time.join(':')

    return resultDate
  }

  static AddFormInput(obj, val) {
    var array = val != null ? val : [];
    if(array.length == 0) {
        return obj;
    }

    array.forEach(item => {
        obj.push(item)
    });

    return obj;
  }

  static getHashText(text) {
    if(!text) return text;

    const md5 = this.crypto.createHash('md5')
    md5.update(text)
    const encoding = 'hex' // hexadecimal(16進数)
    return md5.digest(encoding)
  }

  static splitPythonDic(list) {
    let array = list.replace(/{|}|\s/g, '')
    if(array.length == 0) {
      return null;
    }

    return array.replace(/'|\s/g, '').split(',')
  }

  static createChartMapData(data) {
    if(data == null) {
      return null
    }
    var yearDay = 30 * 12
    var map = new Map();
    data.forEach(x => {
      var val = x.split(':');
      map.set(`${val[0]}`, (Math.round(parseInt(val[1]) / yearDay * 10)) / 10)
    });

    return map;
  }

}

export default (context, inject) => {
  inject('utils', Utils);
}
