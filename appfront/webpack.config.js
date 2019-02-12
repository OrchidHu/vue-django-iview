//1.引入 webpack模块
const webpack = require('webpack');
const path = require('path');
// 抽离css样式---将文件单独打包
const ExtractTextPlugin = require('extract-text-webpack-plugin')

//2.使用webpack 内置的插件, 提取公共代码
const commonsPlugin = new webpack.optimize.CommonsChunkPlugin('common.js');

const extractCssPlugin = new ExtractTextPlugin({
    filename:path.resolve(__dirname, 'dist/css/[name].css'),
    disabled:process.env.NODE_ENV === "deverlopment"
})

const UglifyJSPlugin = require('uglifyjs-webpack-plugin')
 //模块化
module.exports = {
    //3.插件项---要使用的插件放这里，如压缩代码
    plugins: [
        commonsPlugin,
        extractCssPlugin,
        new UglifyJSPlugin({
            uglifyOptions: {
              ie8: false,
              ecma: 8,
              parse: {...options},
              mangle: {
                ...options,
                properties: {
                  // mangle property options
                }
              },
              output: {
                comments: false,
                beautify: false,
                ...options
              },
              compress: {...options},
              warnings: false
            }
        })
    ],

    //4.页面入口文件配置---设置入口文件
    entry: {
        test1 : './js/page1/ab_entry.js',
        test2 : './js/page2/ey_entry.js',
    },

    //5.入口文件输出配置
    output: {
        path: path.resolve(__dirname, 'dist/js'),
        filename: '[name].js'
    }
,
    //6.加载器配置----它告知 webpack 每一种文件都需要使用什么加载器来处理
    module: {
        //加载器配置，需要的加载去通过npm install XXX下载的node_module中
        rules: [
                { test: /\.css$/,
                use:ExtractTextPlugin.extract({
                            // use style-loader in deverlopment
                            fallback: 'style-loader',
                            use:['css-loader','sass-loader','postcss-loader']
                            // use:[{loader:'css-loader'},{loader:'sass-loader'},{loader:'postcss-loader'}]
                }),
            }]
    },

    //7.其它
    resolve: {
        root: 'E:/github/flux-example/src', //绝对路径
        extensions: ['*', '.js', '.json', '.scss'],//自动扩展文件后缀名，意味着我们require模块可以省略不写后缀名
        alias: {//模块别名定义，方便后续直接引用别名，无须多写长长的地址
            AppStore : 'js/stores/AppStores.js',//后续直接 require('AppStore') 即可
            ActionType : 'js/actions/ActionType.js',
            AppAction : 'js/actions/AppAction.js'
        }
    }
};