$.ajaxSetup({
  beforeSend: function beforeSend(xhr, settings) {
    function getCookie(name) {
      let cookieValue = null

      if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')

        for (let i = 0; i < cookies.length; i += 1) {
          const cookie = jQuery.trim(cookies[i])

          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === `${name}=`) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
            break
          }
        }
      }

      return cookieValue
    }

    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
      // Only send the token to relative URLs i.e. locally.
      xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    }
  },
})

$(document)
  .on('click', '.js-toggle-modal', function (e) {
    e.preventDefault()

    $('.js-modal').toggleClass('hidden')
  })
  .on('click', '.js-submit', function (e) {
    e.preventDefault()

    console.log('submitting')

    const $btn = $(this)
    const $textarea = $('.js-post-text')
    const text = $textarea.val().trim()

    if (!text.length) return

    $btn.prop('disabled', true).text('Posting..')

    $.ajax({
      type: 'POST',
      url: $textarea.data('post-url'),
      data: {
        text,
      },
      success: (dataHtml) => {
        $('.js-modal').addClass('hidden')
        $('#post-container').prepend(dataHtml)
        $btn.prop('disabled', false).text('Create post')
        $textarea.val('')
      },
      error: (error) => {
        console.warn("Error submitting the 'Create Post' form: ", error)
        $btn.prop('disabled', false).text('Error')
      },
    })
  })
  .on('click', '.js-follow', function (e) {
    e.preventDefault()

    console.log('following')

    $(this).prop('disabled', true)

    const action = $(this).attr('data-action') //this is not going to be cached as when using $(this).data('action')
    const totalFollowersHolder = $('.js-total-followers-text')

    $.ajax({
      type: 'POST',
      url: $(this).data('url'),
      data: {
        action,
        username: $(this).data('username'),
      },
      success: (data) => {
        $(this).prop('disabled', false)
        $('.js-follow-text').text(data.wording)

        if (action === 'follow') {
          $(this).attr('data-action', 'unfollow')
          totalFollowersHolder.text(
            (parseInt(totalFollowersHolder.text()) + 1).toString()
          )
        } else {
          $(this).attr('data-action', 'follow')
          const total = parseInt(totalFollowersHolder.text())
          totalFollowersHolder.text((total > 0 ? total - 1 : 0).toString())
        }
      },
      error: (error) => {
        console.warn('Error Following User: ', error)
        $(this).prop('disabled', false)
        $('.js-follow-text').text('Error')
      },
    })
  })
// .on('click', '#profile-form > button', function (e) {
//   e.preventDefault()
//   $.ajax({
//     type: 'POST',
//     url: $('#profile-form').data('url'),
//     data: $('#profile-form').serialize(),
//     success: function (response) {
//       // Handle success
//       console.log(response)
//     },
//     error: function (xhr, status, error) {
//       // Handle errors
//       console.log(xhr)
//     },
//   })
// })

$(document).ready(function () {
  $('#id_image').change(function () {
    console.log('changing image')
    const file = $(this)[0].files[0]
    const reader = new FileReader()

    reader.onload = function (e) {
      $('#image-preview').attr('src', e.target.result)
    }

    reader.readAsDataURL(file)
  })
})
