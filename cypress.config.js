const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8000',
    defaultCommandTimeout: 10000, // Увеличьте до 10 секунд
    responseTimeout: 30000, // Увеличьте таймаут ответа
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
})