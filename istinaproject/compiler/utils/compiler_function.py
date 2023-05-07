policy = {'alias': 'authority',
          'nodes': ''}

def cool_print(name, obj):
    print(f'[>>>] {name}:\n\t\t{obj}\n\n')

# True, если суперюзер + автор статьи
def compiler_function(source, label, dest, policy):
    cool_print('source', source)
    cool_print('source.objects', source.objects)
    cool_print('source.objects.all', source.objects.all())
    cool_print('dest', dest)
    cool_print('dest.objects', dest.objects)
    cool_print('dest.objects.all', dest.objects.all())


    restrictions = dict()
    restrictions['is_superuser'] = True
    superusers = source.objects.filter(**restrictions)

    cool_print('papers_related_to_superuser', superusers.paper_set.all())
    cool_print('source.objects.filter', superusers)
    cool_print('superusers_methods', source._meta.get_fields())
    cool_print('papers_methods', dest._meta.get_fields())
    
    
    #print(f1, f1.objects, sep='\n\n', end='\n\n\n')