<template>
    <div class="login-view">
        <div class="form">
          <el-form ref="form" @submit="onLogin" :model="form" autocomplete="off">
            <el-form-item id="input-1" label="ID">
              <el-input v-model="form.id"></el-input>
              <p class="errorMsg">{{this.validErr.inputIdErr}}</p>
            </el-form-item>
            <el-form-item id="input-group-2" label="パスワード">
              <el-input type="password" v-model="form.password" show-password></el-input>
              <p class="errorMsg">{{this.validErr.inputPasswordErr}}</p>
            </el-form-item>
            <el-form-item>
              <div class="login-button">
                <el-button type="primary" @click="onLogin">ログイン</el-button>
              </div>
            </el-form-item>
          </el-form>
        </div>
    </div>
</template>

<script>
export default {
    name: "Login",
    components: {
    },
    props: {
    },
    data() {
        return {
        form: {
            id:'',
            password: '',
        },
        isValidSuccess: true,
        validErr: {inputIdErr: '', inputPasswordErr: ''},
        }
    },
    beforeCreated() {
    },
    created() {
    },
    beforeMount() {
    },
    mounted() {
    },
    beforeUpdate() {
    },
    updated() {
    },
    beforeDestroy() {
    },
    destroyed() {
    },
    methods:{
        onLogin(evt) {
            // バリデーションエラーメッセージをクリア
            this.ValidErrMsgClear();

            // ID入力チェック
            if(this.form.id.trim() == '') {
                this.validErr.inputIdErr = 'IDが入力されていません。';
                this.SetValidErr();
            }
            // パスワード入力チェック
            if(this.form.password.trim() == '') {
                this.validErr.inputPasswordErr = 'パスワードが入力されていません。';
                this.SetValidErr();
            }
            if(!this.isValidSuccess) {
                return;
            }

            var passwordHash = this.$utils.getHashText(this.form.password);
            var params = {'user_id':this.form.id, 'password':passwordHash};
            this.$apiService.doLogin(params, (res) => {
              this.loginSuccess();
            })

            evt.preventDefault();
        },
        // バリデーション初期化
        ValidErrMsgClear() {
            this.validErr.inputIdErr = '';
            this.validErr.inputPasswordErr = '';
            this.isValidSuccess = true;
        },
        // バリデーションエラーセット
        SetValidErr() {
            this.isValidSuccess = false;
        },
        loginSuccess() {
            scrollTo(0, 0);
            this.$router.push(this.$router.options.routes[1]);
        }
    }
}
</script>

<style scoped>
.login-view .form {
  max-width: 60%;
  margin-top: 10rem;
  margin-left: 20%;
}

.login-button {
  text-align: center;
}
</style>
