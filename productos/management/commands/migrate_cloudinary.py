from django.core.management.base import BaseCommand
from django.conf import settings
import os
import cloudinary.uploader
from productos.models import Instrumento

class Command(BaseCommand):
    help = 'Migra imágenes locales de instrumentos a Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecuta una simulación sin realizar cambios reales',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('🔍 Ejecutando en modo DRY RUN - No se realizarán cambios')
            )
        
        # Verificar configuración de Cloudinary
        if not all([
            getattr(settings, 'CLOUDINARY_STORAGE', {}).get('CLOUD_NAME'),
            getattr(settings, 'CLOUDINARY_STORAGE', {}).get('API_KEY'),
            getattr(settings, 'CLOUDINARY_STORAGE', {}).get('API_SECRET')
        ]):
            self.stdout.write(
                self.style.ERROR('❌ Error: Configuración de Cloudinary incompleta')
            )
            self.stdout.write('Asegúrate de tener configuradas las variables:')
            self.stdout.write('- CLOUDINARY_CLOUD_NAME')
            self.stdout.write('- CLOUDINARY_API_KEY')
            self.stdout.write('- CLOUDINARY_API_SECRET')
            return

        instrumentos = Instrumento.objects.all()
        migrated_count = 0
        error_count = 0
        
        self.stdout.write(f"🚀 Iniciando migración de {instrumentos.count()} instrumentos a Cloudinary...")
        
        for instrumento in instrumentos:
            if instrumento.imagen and hasattr(instrumento.imagen, 'path'):
                try:
                    # Verificar si el archivo existe localmente
                    if os.path.exists(instrumento.imagen.path):
                        self.stdout.write(f"📤 Procesando: {instrumento.nombre}")
                        
                        if not dry_run:
                            # Subir a Cloudinary
                            response = cloudinary.uploader.upload(
                                instrumento.imagen.path,
                                folder="instrumentos",
                                public_id=f"instrumento_{instrumento.id}_{instrumento.slug}",
                                overwrite=True,
                                resource_type="image"
                            )
                            
                            # Actualizar la URL en el modelo
                            old_image = instrumento.imagen.name
                            instrumento.imagen = response['secure_url']
                            instrumento.save()
                            
                            self.stdout.write(
                                self.style.SUCCESS(f"✅ Migrado: {instrumento.nombre}")
                            )
                            self.stdout.write(f"   📁 Antes: {old_image}")
                            self.stdout.write(f"   ☁️  Ahora: {response['secure_url']}")
                        else:
                            self.stdout.write(f"   📁 Se migraría: {instrumento.imagen.path}")
                        
                        migrated_count += 1
                        
                    else:
                        self.stdout.write(
                            self.style.WARNING(f"⚠️  Archivo no encontrado: {instrumento.imagen.path}")
                        )
                        error_count += 1
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"❌ Error procesando {instrumento.nombre}: {str(e)}")
                    )
                    error_count += 1
            else:
                self.stdout.write(f"⚠️  Sin imagen: {instrumento.nombre}")
        
        # Resumen final
        self.stdout.write("\n" + "="*50)
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"🔍 SIMULACIÓN COMPLETADA:"))
            self.stdout.write(f"   📊 Se migrarían: {migrated_count} imágenes")
        else:
            self.stdout.write(self.style.SUCCESS(f"🎉 MIGRACIÓN COMPLETADA:"))
            self.stdout.write(f"   ✅ Migradas: {migrated_count} imágenes")
        self.stdout.write(f"   ❌ Errores: {error_count}")
        
        if not dry_run and migrated_count > 0:
            self.stdout.write("\n" + self.style.SUCCESS("🚀 ¡Las imágenes están ahora en Cloudinary!"))
            self.stdout.write("💡 Puedes hacer deploy a producción cuando quieras.")
