from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache

from flatblocks.settings import CACHE_PREFIX

class BlockSet(models.Model):
    """
    A blockset is the flatblock equivalent to Wordpress dynamic sidebars.
    By including one template tag with the blockset's slug, you can
    add a handful of flatblocks in the same place without having to
    keep modifying your templates.
    """
    slug = models.CharField(max_length=255, unique=True,
                verbose_name=_('Slug'),
                help_text=_("A unique name used for reference in the templates"))
    header = models.CharField(blank=True, null=True, max_length=255,
                verbose_name=_('Header'),
                help_text=_("An optional header for this blockset"))
    
    def __unicode__(self):
        return u"%s" % (self.slug,)

    # hope this works...
    def save(self, *args, **kwargs):
        super(BlockSet, self).save(*args, **kwargs)
        # Now also invalidate the cache used in the templatetag
        cache.delete('%s%s' % (CACHE_PREFIX, self.slug, ))

    class Meta:
        verbose_name = _('block set')
        verbose_name_plural = _('block sets')

class FlatBlock(models.Model):
    """
    Think of a flatblock as a flatpage but for just part of a site. It's
    basically a piece of content with a given name (slug) and an optional
    title (header) which you can, for example, use in a sidebar of a website.
    """
    slug = models.CharField(max_length=255, unique=True, 
                verbose_name=_('Slug'),
                help_text=_("A unique name used for reference in the templates"))
    header = models.CharField(blank=True, null=True, max_length=255,
                verbose_name=_('Header'),
                help_text=_("An optional header for this content"))
    content = models.TextField(verbose_name=_('Content'), blank=True, null=True)

    def __unicode__(self):
        return u"%s" % (self.slug,)
    
    def save(self, *args, **kwargs):
        super(FlatBlock, self).save(*args, **kwargs)
        # Now also invalidate the cache used in the templatetag
        cache.delete('%s%s' % (CACHE_PREFIX, self.slug, ))

    class Meta:
        verbose_name = _('Flat block')
        verbose_name_plural = _('Flat blocks')

class BlockSetItem(models.Model):
    """
    This is a model specifically for keeping items in blocksets in
    order. It's just not quite enough to just include FlatBlock as
    a ManyToManyField in the BlockSet model.
    """
    position = models.PositiveIntegerField()
    blockset = models.ForeignKey(BlockSet, verbose_name=_("Associated block set"))
    flatblock = models.ForeignKey(FlatBlock, verbose_name=_("Flat block"))
    
    def __unicode__(self):
        return u"%s" % (self.flatblock.slug,)
