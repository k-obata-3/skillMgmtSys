class ApiService {
  onError = false;

  constructor (axios, utils) {
    this.axios = axios;
    this.utils = utils;
  }

  BASE_URL = '';

  async doLogin (params, callback) {
    const url = `${this.BASE_URL}/login`;
    var vm = this;
    await this.axios.post(url, params)
    .then(response => {
      vm.utils.saveLoginInfo(response.data.user.id, response.data.user.auth);
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getLoginUserInfo(callback) {
    const url = `${this.BASE_URL}/selfUserInfoRetrieve`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async updateLoginUserInfo(param, callback) {
    const url = `${this.BASE_URL}/selfUserInfoUpdate`;
    await this.axios.put(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async updatePassword(param, callback) {
    const url = `${this.BASE_URL}/passwordUpdate`;
    await this.axios.put(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async resetPassword(id, param, callback) {
    const url = `${this.BASE_URL}/passwordReset/?user_id=${id}`;
    await this.axios.put(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getUserInfo(id, callback) {
    const url = `${this.BASE_URL}/userInfoRetrieve/?user_id=${id}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getDepartmentList(callback) {
    const url = `${this.BASE_URL}/departmentList`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async createDepartment(param, callback) {
    const url = `${this.BASE_URL}/departmentCreate`;
    await this.axios.post(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async deleteDepartment(id, callback) {
    const url = `${this.BASE_URL}/departmentDestroy?id=${id}`;
    await this.axios.delete(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getCareerInfo(id, callback) {
    const url = `${this.BASE_URL}/careerInfoRetrieve/?id=${id}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getCareerInfoList(id, limit, offset, callback) {
    const url = `${this.BASE_URL}/careerInfoList/?user_id=${id}&limit=${limit}&offset=${offset}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getCareerInfoAllList(callback) {
    const url = `${this.BASE_URL}/careerInfoAllList`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getUserInfoList(limit, offset, callback) {
    const url = `${this.BASE_URL}/userInfoList/?limit=${limit}&offset=${offset}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getUserInfoExcludeSelfList(limit, offset, callback) {
    const url = `${this.BASE_URL}/userInfoExcludeSelfList/?limit=${limit}&offset=${offset}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async createUser(param, callback) {
    const url = `${this.BASE_URL}/userCreate`;
    await this.axios.post(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getCareerInfoDic(id, callback) {
    const url = `${this.BASE_URL}/careerInfoDicRetrieve/?user_id=${id}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async updateUserInfo(id, param, callback) {
    const url = `${this.BASE_URL}/userInfoUpdate/?user_id=${id}`;
    await this.axios.put(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async createCareerInfo(param, callback) {
    const url = `${this.BASE_URL}/careerInfoCreate`;
    await this.axios.post(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async updateCareerInfo(param, callback) {
    const url = `${this.BASE_URL}/careerInfoUpdate`;
    await this.axios.put(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async deleteCareerInfo(id, callback) {
    const url = `${this.BASE_URL}/careerInfoDestroy/?id=${id}`;
    await this.axios.delete(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getProjectList(limit, offset, callback) {
    const url = `${this.BASE_URL}/projectList/?limit=${limit}&offset=${offset}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getProjectInfo(id, callback) {
    const url = `${this.BASE_URL}/projectRetrieve/?project_id=${id}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async createProject(param, callback) {
    const url = `${this.BASE_URL}/projectCreate`;
    await this.axios.post(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async updateProject(param, callback) {
    const url = `${this.BASE_URL}/projectUpdate`;
    await this.axios.put(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async deleteProject(id, callback) {
    const url = `${this.BASE_URL}/projectDestroy/?id=${id}`;
    await this.axios.delete(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getMasterItemList(key, callback) {
    const url = `${this.BASE_URL}/masterItemList/?key=${key}`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async getMasterItemAllList(callback) {
    const url = `${this.BASE_URL}/masterItemAllList`;
    await this.axios.get(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async createMasterItem(param, callback) {
    const url = `${this.BASE_URL}/masterItemCreate`;
    await this.axios.post(url, param)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async deleteMasterItem(id, callback) {
    const url = `${this.BASE_URL}/masterItemDestroy?id=${id}`;
    await this.axios.delete(url)
    .then(response => {
      callback(response.data);
    })
    .catch(err => {

    })
    .finally(() => {
    });
  }

  async outputCareerInfo(id, callback) {
    const url = `${this.BASE_URL}/careerInfoOutput/?user_id=${id}`;
    await this.axios.get(url, {
      responseType:'arraybuffer',
    })
    .then(response => {
      if(response.headers['content-type'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
        let blob = new Blob([response.data], {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,"});
        let link = document.createElement('a');
        let url = window.URL.createObjectURL(blob);
        let disposition = response.headers['content-disposition'];
        let fileName = null;

        // 正規表現でfilenameを抜き出す
        const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
        const matches = filenameRegex.exec(disposition);
        if (matches != null && matches[1]) {
            const fName = matches[1].replace(/['"]/g, '');
            fileName = decodeURI(fName);
        }

        link.href = url;
        link.download = fileName;
        link.click()
     }
    })
    .catch(err => {

    })
    .finally(() => {
      callback();
    });
  }
}

export default (context, inject) => {
  context.$axios.onRequest((config) => {
    context.$axios.defaults.headers.common['Access-Control-Allow-Credentials'] = 'true';
    return config;
  })
  context.$axios.onError(err => {
    if (err.response == null) {
      return;
    }

    let res = JSON.parse(JSON.stringify(err.response));
    let errMsg = '';

    if(res.status == 403) {
      // 認証エラー
      errMsg = '認証エラー';
    } else if(res.config.responseType == 'arraybuffer') {
      // ファイルダウンロードエラー
      errMsg = '経歴情報のダウンロードに失敗しました';
    } else {
      errMsg = res.data['data'];
    }

    context.app.store.commit('setErrorMsg', errMsg);
  })

  inject('apiService', new ApiService(context.$axios, context.$utils));
}