# Скрипт по синхранизации базы локальной и серверной
def mysql(git, warn_only=True, cache=None):
    if git in denided_list:
        print('Denided')
    else:
        local('mysqldump -u user -ppass {0} > /home/project/{0}/{0}.sql'.format(git))
        with lcd('$HOME/git/{}'.format(git)):
            try:
                local('git add -A')
                local('git commit -m "skip"')
                local('git push origin master')
            except BaseException as e:
                print e
        env.user = '%s' % git
        env.port = 12345
        env.host_string = 'google.com'
        env.key_filename = [os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')]
        with cd('/home/%s' % git):
            run('git pull origin master')
        if git == 'pr':
            pw = 'pass'
        run("mysql -u {0} -p'{1}' {0} < /home/{0}/django/{0}.sql".format(git, pw))
        run('touch ~/uwsgi/reload')
        
        
# Скрипт выполнения каких-то команд
@_contextmanager
def thumb(git):
    with lcd('$HOME/proj/{}'.format(git)):
        with prefix('source $HOME/.env/{}/bin/activate'.format(git)):
            local('rm -rf media/cache', shell='/bin/bash')
            local('./manage.py thumbnail cleanup', shell='/bin/bash')
            local('./manage.py thumbnail clear', shell='/bin/bash')
            local('mkdir media/cache', shell='/bin/bash')
            
# форма Django с условием на заполненость полей, с отправкой на почту и с двумя кнопками в форме
    if request.method == "POST":
        if request.GET.has_key('id'):
            object_to_edit = get_object_or_404(Reserv, id=request.GET.get('id'))
            form = FormReservBig(request.POST, instance=object_to_edit)
        else:
            form = FormReservBig(request.POST)
        if form.is_valid():
            new_form = form.save()
            ctx = {
                'name': form.cleaned_data.get('name').encode('utf-8'),
                'contact': form.cleaned_data.get('contact').encode('utf-8'),
                'date_in': form.cleaned_data.get('date_in'),
                'date_out': form.cleaned_data.get('date_out'),
                'category': form.cleaned_data.get('category'),
                'deposit': form.cleaned_data.get('deposit')
            }
            summa = (ctx['date_out'] - ctx['date_in']).days
            room = Room.objects.get(tt=ctx['category'])
            subject = u'Заказ на сумму: $%s' % (room.price * summa)
            message = render_to_string('mail.txt', ctx)
            to = settings.LIST_OF_EMAIL_RECIPIENTS
            EmailMessage(subject, message, to=to, from_email = 'example').send()
            if 'go_reserv' in request.POST:
                pass
                return render(request, 'app/vw_booking.html', {'form': form, 'flag': True})
            elif 'go_pay' in request.POST:
                return HttpResponseRedirect(reverse('app:vw_demir', args=[new_form.pk]))
                
                
# парсинг Демир Банка
    obj = get_object_or_404(Reserv, pk=pk)
    room_cost = Room.objects.get(tt=obj.category).price_som
    days = (obj.date_out - obj.date_in).days
    amount_total = room_cost * days

    amount_full = False
    if obj.deposit:
        amount = obj.deposit
        amount_full = amount_total
    else:
        amount = amount_total

    current_site = Site.objects.get_current()

    rnd = uuid.uuid4().hex[:20]
    go_pay = {
      ...
    }

    hash_fields = ['clientid', 'oid', 'amount', 'okUrl', 'failUrl', 'islemtipi', 'taksit', 'rnd', 'storekey']
    hash_str = ''.join([str(go_pay[f]) for f in hash_fields])
    hash = base64.b64encode(hashlib.sha1(hash_str).digest())
    go_pay['hash_str'] = hash_str
    go_pay['hash'] = hash

    form = FormDemir(request.POST)
    obj.demir = str(go_pay)
    obj.save()

# убираем фон в PNG
def create(self, image, geometry, options):
    im = super(Engine, self).create(image, geometry, options)
    if options.get('background'):
        try:
            background = Image.new('RGB', im.size, ImageColor.getcolor(options.get('background'), 'RGB'))
            background.paste(im, mask=im.split()[3])  # 3 is the alpha of an RGBA image.
            return background
        except Exception:
            return im
    return im

#счетчик посещений
def PostLogCount():
    os.rename(STATIC_ROOT + "/real.log", STATIC_ROOT + "/real_.log")
    RealLog = open(STATIC_ROOT + "/real_.log","r")
    for linelog in RealLog.readlines():
        real = Real.objects.get(id=linelog)
        if real:
           real.displays = story.displays + 1
        real.save()
    RealLog.close
    os.remove(STATIC_ROOT + "/real_.log")

#watermark
fh = storage.open(self.image.name, 'r')
img = PIL.Image.open(fh)
watermark_name, watermark_extension = os.path.splitext(self.image.name)
watermark_extension = watermark_extension.lower()
watermark_filename = watermark_name + '_watermark' + watermark_extension

if watermark_extension in ['.jpg', '.jpeg']:
    FTYPE = 'JPEG'
elif watermark_extension == '.gif':
    FTYPE = 'GIF'
elif watermark_extension == '.png':
    FTYPE = 'PNG'
else:
    return False  # Unrecognized file type

width, height = img.size
draw = PIL.ImageDraw.Draw(img)
font = PIL.ImageFont.truetype(_font_as_bytes(), 13)
text = [u"Бишкек, Медерова", u"hotel.kg", u"+996 779 99 99 99"]

for num, line in enumerate(text):
    textwidth, textheight = draw.textsize(line, font)

    margin = 15
    x = width - textwidth - margin
    y = height - textheight - margin * num

    draw.text((x - 1, y - 11), line, font=font, fill='#3b4947')
    draw.text((x, y - 10), line, font=font, fill='#fff')

temp_watermark = StringIO()
img.save(temp_watermark, FTYPE)
temp_watermark.seek(0)

self.image_watermark.save(watermark_filename, ContentFile(temp_watermark.read()), save=True)
temp_watermark.close()
