Cypress.Commands.add('login', (username, password) => {
  cy.session([username, password], () => {
    cy.visit('/admin/login/')
    cy.get('#id_username').should('be.visible').type(username)
    cy.get('#id_password').should('be.visible').type(password)
    cy.get('input[type="submit"]').click()

    // Проверяем успешный вход по наличию элемента в админке
    cy.get('#user-tools', { timeout: 10000 }).should('be.visible')
  })
})