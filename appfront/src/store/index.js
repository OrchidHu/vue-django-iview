import Vue from 'vue'
import Vuex from 'vuex'
import { setToken, setUserName, setSessionId } from '@/libs/util'
import { login, logout } from '@/api/user'
import app from './module/app'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    userName: '',
    avator: '',
    token: '',
    sessionId: '',
    task: []
  },
  mutations: {
    setAvator (state, avatorPath) {
      state.avator = avatorPath
    },
    setUserName (state, name) {
      state.userName = name
      setUserName(name)
    },
    setToken (state, token) {
      state.token = token
      setToken(token)
    },
    setSessionId (state, sessionId) {
      state.sessionId = sessionId
      setSessionId(sessionId)
    },
    setTask (state, message) {
      state.task.push(message)
    },
    clearTask (state, message) {
      state.task = message
    }
  },
  actions: {
    // 登录
    handleLogin ({ commit }, {userName, password}) {
      userName = userName.trim()
      return new Promise((resolve, reject) => {
        login({
          userName,
          password
        }).then(res => {
          const data = res.data
          if (res.data.stat === 'success') {
            commit('setToken', data.token)
            commit('setSessionId', data.session_id)
            commit('setUserName', data.username)
            commit('setAvator', data.avator)
            localStorage.setItem('userAvator', data.avator)
          }
          resolve(data)
        }).catch(err => {
          reject(err)
        })
      })
    },
    // 退出登录
    handleLogOut ({ state, commit }) {
      return new Promise((resolve, reject) => {
        logout(state.token).then(() => {
          commit('setToken', '')
          commit('setSessionId', '')
          commit('setUserName', '')
          commit('clearTask', [])
          resolve()
        }).catch(err => {
          reject(err)
        })
        // 如果你的退出登录无需请求接口，则可以直接使用下面三行代码而无需使用logout调用接口
        // commit('setToken', '')
        // commit('setAccess', [])
        // resolve()
      })
    }
    // 获取用户相关信息
    //    getUserInfo ({ state, commit }) {
    //      return new Promise((resolve, reject) => {
    //        try {
    //          getUserInfo(state.token).then(res => {
    //            const data = res.data
    //            commit('setAvator', data.avator)
    //            commit('setUserName', data.user_name)
    //            commit('setUserId', data.user_id)
    //            commit('setAccess', data.access)
    //            commit('setHasGetInfo', true)
    //            resolve(data)
    //          }).catch(err => {
    //            reject(err)
    //          })
    //        } catch (error) {
    //          reject(error)
    //        }
    //      })
    //    }
  },
  modules: {
    app
  }
})
