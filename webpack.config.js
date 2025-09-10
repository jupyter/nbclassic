const path = require('path');
const crypto = require('crypto');
const CopyWebpackPlugin = require('copy-webpack-plugin');

// Workaround for loaders using "md4" by default, which is not supported in FIPS-compliant OpenSSL
// See https://github.com/jupyterlab/jupyterlab/issues/11248
const cryptoOrigCreateHash = crypto.createHash;
crypto.createHash = (algorithm) =>
  cryptoOrigCreateHash(algorithm == 'md4' ? 'sha256' : algorithm);

const mainConfig = {
  name: 'mainConfig',
  entry: ['babel-polyfill', '@jupyterlab/apputils/lib/sanitizer'],
  output: {
    filename: 'index.js',
    path: path.resolve(__dirname, 'nbclassic/static/components/sanitizer'),
    libraryTarget: "amd",
  },
  devtool: false,
  optimization: {
    minimize: false
  },
  module: {
    rules: [
      {
        test: /\.m?jsx?$/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          }
        }
      }
    ]
  }
}

const nb6Config = {
  name: 'nb6Config',
  mode: 'production',
  entry: {},
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        // Same content, different path/name for NB6-style consumers:
        {
          from: path.resolve(__dirname, 'nbclassic/static/components/react/umd/react.production.min.js'),
          to: path.resolve(__dirname, 'nbclassic/static/components/react/react.production.min.js'),
        },
        {
          from: path.resolve(__dirname, 'nbclassic/static/components/react-dom/umd/react-dom.production.min.js'),
          to: path.resolve(__dirname, 'nbclassic/static/components/react/react-dom.production.min.js'),
        },
        {
          from: path.resolve(__dirname, 'nbclassic/static/components/es6-promise/dist/promise-1.0.0.min.js'),
          to: path.resolve(__dirname, 'nbclassic/static/components/es6-promise/promise.min.js'),
        },
        {
          from: path.resolve(__dirname, 'nbclassic/static/components/jquery/dist/jquery.min.js'),
          to: path.resolve(__dirname, 'nbclassic/static/components/jquery/jquery.min.js'),
        }
      ],
    }),
  ],
  // ensure this runs after 'main'
  dependencies: ['mainConfig'],
};

module.exports = [mainConfig, nb6Config];
