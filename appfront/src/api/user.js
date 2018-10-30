import axios from '@/libs/api.request'
import config from '@/config'

export const login = ({ userName, password }) => {
const username = userName
  const data = {
    username,
    password
  }
  return axios.request({
    url: config.loginUrl,
    data,
    method: 'post'
  })
}

//export const getUserInfo = (token) => {
//  return axios.request({
//    url: 'get_info',
//    params: {
//      token
//    },
//    method: 'get'
//  })
//}

export const logout = (token) => {
  return axios.request({
    url: config.logoutUrl,
    method: 'get',
    withCredentials: true
  })
}
