policy = {'alias': 'authority',
          'nodes': ''}

def cool_print(name, obj):
    print(f'[>>>] {name} ({str(type(obj))[:30]}):\n\t\t{obj}\n\n')

# True, если суперюзер + автор статьи
def compiler_function(source, label, dest, policy):
    print('+'*40 + '\n\n')
    cool_print('source', source)
    cool_print('source.objects', source.objects)
    cool_print('source.objects.all', source.objects.all())
    cool_print('dest', dest)
    cool_print('dest.objects', dest.objects)
    cool_print('dest.objects.all', dest.objects.all())

    restrictions = dict()
    restrictions['is_superuser'] = True
    back_relation = 'users_of_paper'
    superusers = source.objects.filter(**restrictions)

    cool_print('source.objects.filter', superusers)
    cool_print('superusers_methods', source._meta.get_fields())
    cool_print('source._meta.get_field("papers_of_user")', source._meta.get_field('papers_of_user'))
    cool_print('source._meta.get_field("papers_of_user")', source._meta.get_field('users_of_paper'))
    cool_print('papers_methods', dest._meta.get_fields())
    
    
    #print(f1, f1.objects, sep='\n\n', end='\n\n\n')