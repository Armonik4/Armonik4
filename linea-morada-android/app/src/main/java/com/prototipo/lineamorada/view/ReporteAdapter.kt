package com.prototipo.lineamorada.view

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.prototipo.lineamorada.R
import com.prototipo.lineamorada.databinding.ItemReporteBinding
import com.prototipo.lineamorada.model.SolicitudAyuda
import java.text.DateFormat
import java.util.Date
import java.util.Locale

/**
 * VISTA — Dibuja cada reporte del historial.
 *
 * Usa ListAdapter + DiffUtil: al cambiar un estado solo se redibuja esa fila,
 * no toda la lista (rendimiento).
 * El clic se reenvía con `onClick`; la decisión la toma el Controlador.
 *
 * PRUEBA DE UI: revisar con Espresso que la fila muestre tipo, estado y fecha.
 */
class ReporteAdapter(
    private val onClick: (SolicitudAyuda) -> Unit,
) : ListAdapter<SolicitudAyuda, ReporteAdapter.ReporteViewHolder>(DIFF) {

    private val formatoFecha: DateFormat = DateFormat.getDateTimeInstance(
        DateFormat.MEDIUM,
        DateFormat.SHORT,
        Locale.forLanguageTag("es-CO"),
    )

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ReporteViewHolder {
        val binding = ItemReporteBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ReporteViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ReporteViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    inner class ReporteViewHolder(
        private val binding: ItemReporteBinding,
    ) : RecyclerView.ViewHolder(binding.root) {

        fun bind(reporte: SolicitudAyuda) {
            val contexto = binding.root.context
            binding.tvTipo.text = contexto.getString(
                R.string.item_tipo,
                reporte.tipoApoyo.etiqueta,
                reporte.tipoViolencia.etiqueta,
            )
            binding.tvEstado.text = reporte.estado.etiqueta
            binding.tvDescripcion.text = reporte.descripcion
            binding.tvMeta.text = contexto.getString(
                R.string.item_meta,
                formatoFecha.format(Date(reporte.marcaTiempo)),
                reporte.ubicacionAproximada.ifEmpty { contexto.getString(R.string.sin_ubicacion) },
            )
            binding.root.setOnClickListener { onClick(reporte) }
        }
    }

    private companion object {
        val DIFF = object : DiffUtil.ItemCallback<SolicitudAyuda>() {
            override fun areItemsTheSame(a: SolicitudAyuda, b: SolicitudAyuda) = a.id == b.id
            override fun areContentsTheSame(a: SolicitudAyuda, b: SolicitudAyuda) = a == b
        }
    }
}
