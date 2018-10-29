from django.db import models


class Grid(models.Model):
    id = models.IntegerField(primary_key=True, blank=True, null=False)  # AutoField?
    lon = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    country = models.IntegerField(blank=True, null=True)
    altitude = models.IntegerField(blank=True, null=True)
    

    class Meta:
        
        db_table = 'grid'

    def __str__(self):
        return 'lon={0}, lat={1}, country={2}, altitude={3}'.format(self.lon,self.lat,
            self.country, self.altitude)