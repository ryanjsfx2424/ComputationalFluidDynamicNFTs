module.exports = function override (config, env) {
  console.log("override")
  let loaders = config.resolve
  loaders.fallback = {
    "fs": false,
    "os": require.resolve("os-browserify/browser"),
    "path": require.resolve("path-browserify"),
    "http": require.resolve("stream-http"),
    "https": require.resolve("https-browserify"),
    "assert": require.resolve("assert/"),
    "stream": require.resolve("stream-browserify")
  }
  return config
}
