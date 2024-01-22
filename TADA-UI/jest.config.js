module.exports = {
  preset: 'ts-jest',
  globals: {
    'ts-jest': {
      diagnostics: false,
      tsConfig: 'tsconfig.test.json'
    }
  },
  setupFilesAfterEnv:["@testing-library/jest-dom/extend-expect"],
  moduleNameMapper: {
    ".+\\.(jpg|ico|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga|css)$": "identity-obj-proxy"
  },
  
  transformIgnorePatterns: [
    //"node_modules/(?!(antd)/)"
    "/node_modules/(?!antd|@ant-design|rc-.+?|@babel/runtime).+(js|jsx)$",
    
  ]
};