document.addEventListener('DOMContentLoaded', main)

function main() {
    handle_file()
}

function handle_file() {
    file = document.querySelector('.post_image');
    file.addEventListener('change', e => {
        image = e.target.files[0]
        if (image) {
            type = image.type.split('/')[1]

            if (!['jpg', 'png', 'webp', 'jpeg'].includes(type)) {
                alert(`not support this type: ${type}`)
                return
            }

            post_image_box = document.getElementById('post_image-box')

            url = URL.createObjectURL(image)
            post_image_box.setAttribute('src', url)

        }
        
    })
}