const Epub = require("epub-gen")
export function cleanup(html) {

    // replace all <br> to \n
    const contentWithBr = html.replaceAll('<br>', '\n')
    // replace nbsp to space
    const contentWithSpace = contentWithBr.replaceAll('&nbsp;', ' ')
    // add space after p tags
    const contentWithSpaceP = contentWithSpace.replaceAll('</p>', "</p>\n\n")
    // remove all tags
    const contentWithoutTags = contentWithSpaceP.replace(/<\/?[^>]+(>|$)/g, "")

    const textBasic = contentWithoutTags.replace(
        /[\uff01-\uff5e]/g,
        function(ch) { return String.fromCharCode(ch.charCodeAt(0) - 0xfee0) }
    )

    const removedUseless = textBasic.replaceAll('UU看书 www.uukanshu.com', '')
    const removedUseless1 = removedUseless.replaceAll('UU看書 www.uukanshu.com', '')
    const removedUseless2 = removedUseless1.replaceAll('UU看書www.uukanshu.com', '')
    const removedUseless3 = removedUseless2.replaceAll('UU看书www.uukanshu.com', '')
    const addSpace = removedUseless3.replaceAll(',', ', ')
    const addSpace1 = addSpace.replaceAll(':', ': ')
    const replaceDot = addSpace1.replaceAll('。', '.')
    const replaceTripleDot = replaceDot.replaceAll('…', '.')

    const removeAds = replaceTripleDot.replaceAll('(adsbygoogle = window.adsbygoogle || []).push({});', '')

    // remove linebreak if its after a linebreak
    const removeLineBreak = removeAds.replaceAll('\n\n', '\n')

    // remove spaces and linebreaks at the beginning and end of the text
    const trim = removeLineBreak.trim()

    return trim
}

export async function saveBook({ text, title, author, imageUrl, publisher }) {

    // remove all spaces and symbols from fileName
    const fileName = title.replace(',', '_').replace(/\W+/g, '')


    const option = {
        title: title, // *Required, title of the book.
        author: author, // *Required, name of the author.
        publisher: publisher, // optional
        cover: imageUrl,
        content: [
            {
                data: text
            }

        ]
    }

    new Epub(option, `./bin/${fileName}.epub`)
}