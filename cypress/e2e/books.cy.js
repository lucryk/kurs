it('should add a new book from fixture', () => {
  cy.login('klopk', '123123123')

  cy.fixture('books').then((bookData) => {
    const uniqueTitle = `${bookData.title} ${Date.now()}`

    cy.visit('/books/book/add/')

    // 1. Проверяем загрузку формы
    cy.get('form#book-form', { timeout: 10000 })
      .should('be.visible')
      .screenshot('form-loaded') // Скриншот формы

    // 2. Заполняем форму
    cy.get('#id_title').type(uniqueTitle)
    cy.get('#id_author').type(bookData.author)
    cy.get('#id_code').type(bookData.code)
    cy.get('#id_medium').select(bookData.medium)
    cy.get('#id_genre').select(bookData.genre.toString())
    cy.get('#id_year').type(bookData.year)
    cy.get('#id_retail_price').type(bookData.retail_price)
    cy.get('#id_wholesale_price').type(bookData.wholesale_price)
    cy.get('#id_stock').type(bookData.stock)
    cy.get('#id_sold').type(bookData.sold)

    // 3. ПРОВЕРКА CSRF ТОКЕНА
    cy.get('input[name="csrfmiddlewaretoken"]')
      .should('exist')
      .and('not.be.visible')
      .and('not.have.value', '')
      .then(($token) => {
        const tokenValue = $token.val()
        console.log('CSRF Token Value:', tokenValue)
      })

    // 4. Отправляем форму
    cy.get('form#book-form').submit()

    // 5. ПРОВЕРКА ОШИБОК ВАЛИДАЦИИ
    cy.get('body', { timeout: 5000 }).then(($body) => {
      // Проверка общих ошибок
      if ($body.find('.alert-danger').length > 0) {
        const errorText = $body.find('.alert-danger').text()
        throw new Error(`Общие ошибки формы: ${errorText}`)
      }

      // Проверка ошибок полей
      if ($body.find('.text-danger').length > 0) {
        const fieldErrors = $body.find('.text-danger').map((i, el) => el.innerText).get().join('; ')
        throw new Error(`Ошибки полей: ${fieldErrors}`)
      }
    })

    // 6. Проверяем редирект
    cy.url().should('include', '/books/')

    // 7. Проверяем наличие книги
    cy.contains(uniqueTitle, { timeout: 10000 })
      .should('be.visible')
      .screenshot('book-visible') // Скриншот книги в списке
  })
})