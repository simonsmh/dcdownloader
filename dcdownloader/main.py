import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))


from dcdownloader import aiodownloader, base_logger, config, aio_chapter_list, version, jpg2epub
from dcdownloader.utils import update_window_title

import time, json, os

if config.get('debug_mode') == True:
    base_logger.logging_level=base_logger.logging.DEBUG

logger = base_logger.getLogger(__name__)

def get_comic_index_page_url():
    print()
    url = None
    while not url:
        url = input('Index page url of target comic: ')
    print() 
    return url

def main():
    version.show_welcome()
    logger.info('App launch')
    try:
        logger.debug('Load configure file')
        config.load_file('config.yml')
    except Exception as err:
        logger.warning('Failed to load configure file (%s)', str(err))

    if len(sys.argv) > 1:
        index_page_url = sys.argv[1]
    else:
        logger.info('Ask user for enter url')
        index_page_url = get_comic_index_page_url()
    
    logger.info('Fetch chapter list')
    update_window_title(mode='Fetching')
    title, chapter_page_list, cover = aio_chapter_list.parse_comic_chapter_list(index_page_url)

    if len(chapter_page_list) == 0:
        logger.critical('comic url invalid or no chapter avaliable.')
        exit()
    
    update_window_title(mode='Fetching', msg=title)
    logger.info('Comic title: %s' % title)
    logger.info('Fetch each chapter page')
    list_new = {}
    list_new = aio_chapter_list.fetch_all_image_list(chapter_page_list)
    list_new['cover'] = [cover]
    
    output_path = config.get('output_path')
    try:
        if sys.argv[2]:
            output_path = sys.argv[2]
    except:
        pass
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    aiodownloader.launch_downloader(title, list_new, output_path)
    logger.info('All download complete')

    if config.get('epub') == True:
        logger.info('Making epub...')
        with jpg2epub.Jpg2Epub(title, file_name=output_path + "/" + title + ".epub", creator="动漫之家") as j2e:
            coverDir = output_path + "/" + title + "/cover.jpg"
            j2e.add_image_file(coverDir)
            def eachFile(filepath):
                pathDir = os.listdir(filepath)
                for s in pathDir:
                    newDir=os.path.join(filepath,s)
                    if os.path.isfile(newDir):
                        if newDir != coverDir:
                            if os.path.splitext(newDir)[1]==".jpg":
                                j2e.add_image_file(newDir)
                                pass
                            pass
                    else:
                        eachFile(newDir)
            eachFile(output_path + "/" + title)
        logger.info('Done.')

if __name__ == '__main__':
    main()

